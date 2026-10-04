#!/usr/bin/env python3
"""Ship Check scanner: fast, dependency-free production-readiness checks.

Usage:
    python3 scan.py [REPO_PATH] [--format json|markdown] [--fail-on SEVERITY]

Outputs findings the agent then verifies and expands on. Secret values are
always masked in the output.
"""

import argparse
import json
import os
import re
import subprocess
import sys

VERSION = "1.0.0"

SEVERITY_WEIGHT = {"critical": 25, "high": 10, "medium": 4, "low": 1, "info": 0}
SEVERITY_ORDER = ["critical", "high", "medium", "low", "info"]

SKIP_DIRS = {
    ".git", "node_modules", "vendor", "venv", ".venv", "env", "__pycache__",
    "dist", "build", ".next", ".nuxt", "target", "coverage", ".tox",
    ".mypy_cache", ".pytest_cache", ".terraform", "Pods",
}
MAX_SCAN_BYTES = 1_000_000
LARGE_FILE_BYTES = 5_000_000
MAX_LOCATIONS = 10

CODE_EXT = {
    ".js", ".jsx", ".ts", ".tsx", ".mjs", ".cjs", ".py", ".rb", ".go", ".java",
    ".kt", ".php", ".cs", ".rs", ".swift", ".scala", ".vue", ".svelte",
}
JS_EXT = {".js", ".jsx", ".ts", ".tsx", ".mjs", ".cjs", ".vue", ".svelte"}

SECRET_PATTERNS = [
    ("aws-access-key", "AWS access key ID", re.compile(r"\b(AKIA|ASIA)[0-9A-Z]{16}\b")),
    ("private-key", "Private key", re.compile(r"-----BEGIN (?:RSA |EC |DSA |OPENSSH |PGP )?PRIVATE KEY")),
    ("github-token", "GitHub token", re.compile(r"\b(?:gh[pousr]_[A-Za-z0-9]{36,}|github_pat_[A-Za-z0-9_]{60,})\b")),
    ("slack-token", "Slack token", re.compile(r"\bxox[baprs]-[A-Za-z0-9-]{10,}\b")),
    ("stripe-live-key", "Stripe live secret key", re.compile(r"\b[sr]k_live_[A-Za-z0-9]{20,}\b")),
    ("google-api-key", "Google API key", re.compile(r"\bAIza[0-9A-Za-z_\-]{35}\b")),
    ("anthropic-key", "Anthropic API key", re.compile(r"\bsk-ant-[A-Za-z0-9_\-]{20,}\b")),
    ("openai-key", "OpenAI API key", re.compile(r"\bsk-(?:proj-)?[A-Za-z0-9_\-]{32,}\b")),
    ("hardcoded-credential", "Hard-coded credential",
     re.compile(r"""(?i)\b(?:password|passwd|secret|api[_-]?key|access[_-]?token|auth[_-]?token)\b\s*[:=]\s*["']([^"'\s]{8,})["']""")),
]
PLACEHOLDER = re.compile(r"(?i)(example|placeholder|changeme|your[_-]|xxx|dummy|sample|<|\$\{|process\.env|os\.environ|getenv)")

ENV_USAGE = re.compile(r"process\.env\.|os\.environ|os\.getenv\(|ENV\[|System\.getenv|import\.meta\.env\.")
DEBUG_JS = re.compile(r"^\s*(?:console\.log\(|debugger;)")
DEBUG_PY = re.compile(r"^\s*(?:breakpoint\(\)|import pdb|pdb\.set_trace\(\))")
TODO = re.compile(r"\b(TODO|FIXME|HACK|XXX)\b")
CORS_WILDCARD = re.compile(r"""Access-Control-Allow-Origin["']?\s*[:,]\s*["']\*["']|origin\s*:\s*["']\*["']|CORS_ALLOW_ALL_ORIGINS\s*=\s*True""")
DJANGO_DEBUG = re.compile(r"^\s*DEBUG\s*=\s*True\b")


def mask(value):
    if len(value) <= 8:
        return "*" * len(value)
    return value[:4] + "*" * (len(value) - 8) + value[-4:]


def is_test_path(rel):
    parts = rel.lower().replace("\\", "/").split("/")
    name = parts[-1]
    return (
        any(p in ("test", "tests", "__tests__", "spec", "fixtures", "examples") for p in parts[:-1])
        or name.startswith("test_")
        or ".test." in name
        or ".spec." in name
        or name.endswith("_test.go")
    )


def list_files(root):
    """Prefer git's view of the repo (respects .gitignore); fall back to a walk."""
    try:
        out = subprocess.run(
            ["git", "-C", root, "ls-files", "-co", "--exclude-standard", "-z"],
            capture_output=True, check=True, timeout=60,
        ).stdout.decode("utf-8", "replace")
        files = [f for f in out.split("\0") if f]
        files = [f for f in files if not (set(f.split("/")[:-1]) & SKIP_DIRS)]
        if files:
            return files, True
    except (OSError, subprocess.SubprocessError):
        pass
    files = []
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
        for name in filenames:
            files.append(os.path.relpath(os.path.join(dirpath, name), root).replace(os.sep, "/"))
    return files, False


def read_text(path):
    try:
        if os.path.getsize(path) > MAX_SCAN_BYTES:
            return None
        with open(path, "rb") as fh:
            data = fh.read()
    except OSError:
        return None
    if b"\0" in data[:8192]:
        return None
    return data.decode("utf-8", "replace")


class Scanner:
    def __init__(self, root):
        self.root = os.path.abspath(root)
        self.findings = {}
        self.stack = []

    def add(self, fid, severity, category, title, fix, file=None, line=None, detail=None):
        f = self.findings.setdefault(fid, {
            "id": fid, "severity": severity, "category": category, "title": title,
            "fix": fix, "count": 0, "locations": [],
        })
        f["count"] += 1
        if file and len(f["locations"]) < MAX_LOCATIONS:
            loc = {"file": file}
            if line:
                loc["line"] = line
            if detail:
                loc["detail"] = detail
            f["locations"].append(loc)

    def run(self):
        files, in_git = list_files(self.root)
        names = set(files)
        basenames = {f.rsplit("/", 1)[-1].lower() for f in files}
        self.detect_stack(names, basenames)
        self.check_repo_hygiene(files, names, basenames, in_git)

        uses_env = False
        for rel in files:
            path = os.path.join(self.root, rel)
            try:
                size = os.path.getsize(path)
            except OSError:
                continue
            if size > LARGE_FILE_BYTES:
                self.add("large-file", "low", "repo", "Large file committed",
                         "Move large binaries to object storage or Git LFS.",
                         rel, detail=f"{size // 1_000_000} MB")
                continue
            text = read_text(path)
            if text is None:
                continue
            if self.scan_file(rel, text):
                uses_env = True

        env_examples = {".env.example", ".env.sample", ".env.template", "env.example", ".env.dist"}
        if uses_env and not (env_examples & basenames):
            self.add("missing-env-example", "medium", "config", "Code reads environment variables but there is no .env.example",
                     "Add a .env.example listing every required variable with placeholder values.")
        return self.report(len(files))

    def detect_stack(self, names, basenames):
        markers = [
            ("package.json", "Node.js"), ("requirements.txt", "Python"), ("pyproject.toml", "Python"),
            ("go.mod", "Go"), ("cargo.toml", "Rust"), ("gemfile", "Ruby"), ("composer.json", "PHP"),
            ("pom.xml", "Java"), ("build.gradle", "Java/Kotlin"), ("dockerfile", "Docker"),
            ("next.config.js", "Next.js"), ("next.config.mjs", "Next.js"), ("manage.py", "Django"),
        ]
        for marker, label in markers:
            if marker in basenames and label not in self.stack:
                self.stack.append(label)
        if any(n.endswith(".tf") for n in names):
            self.stack.append("Terraform")

    def check_repo_hygiene(self, files, names, basenames, in_git):
        if not any(b.startswith("readme") for b in basenames):
            self.add("missing-readme", "low", "docs", "No README",
                     "Add a README with setup, run, test and deploy instructions.")
        if not any(b.startswith(("license", "licence")) for b in basenames):
            self.add("missing-license", "info", "docs", "No LICENSE file",
                     "Add a LICENSE so users know how the code may be used.")
        if not any(is_test_path(f) for f in files):
            self.add("no-tests", "high", "quality", "No automated tests found",
                     "Add tests for the critical paths (auth, payments, data writes) before shipping.")
        ci = (".github/workflows/", ".gitlab-ci.yml", ".circleci/", "azure-pipelines.yml", "bitbucket-pipelines.yml", "jenkinsfile")
        if not any(f.lower().startswith(ci) or f.lower() in ci for f in files):
            self.add("no-ci", "medium", "quality", "No CI pipeline",
                     "Add CI that runs lint and tests on every push and pull request.")
        if "package.json" in basenames and not ({"package-lock.json", "yarn.lock", "pnpm-lock.yaml", "bun.lockb", "bun.lock"} & basenames):
            self.add("no-lockfile", "medium", "reliability", "package.json without a lockfile",
                     "Commit your package manager's lockfile for reproducible installs.")

        gitignore = os.path.join(self.root, ".gitignore")
        if in_git:
            if not os.path.exists(gitignore):
                self.add("missing-gitignore", "medium", "security", "No .gitignore",
                         "Add a .gitignore that excludes .env files, build output and dependencies.")
            else:
                content = read_text(gitignore) or ""
                if not re.search(r"^\s*/?\.env", content, re.M):
                    self.add("env-not-ignored", "medium", "security", ".env is not listed in .gitignore",
                             "Add `.env` and `.env.*` (with `!.env.example`) to .gitignore.")

        for rel in files:
            base = rel.rsplit("/", 1)[-1]
            if base == ".env" or (base.startswith(".env.") and not base.endswith((".example", ".sample", ".template"))):
                self.add("env-file-committed", "critical", "security", "Environment file committed to the repo",
                         "Remove it from git, rotate every secret it contains, and add it to .gitignore.", rel)

    def scan_file(self, rel, text):
        ext = os.path.splitext(rel)[1].lower()
        base = rel.rsplit("/", 1)[-1]
        test_file = is_test_path(rel)
        uses_env = False

        for lineno, line in enumerate(text.splitlines(), 1):
            if len(line) > 2000:
                continue
            for sid, label, pattern in SECRET_PATTERNS:
                m = pattern.search(line)
                if not m:
                    continue
                value = m.group(1) if m.groups() and sid == "hardcoded-credential" else m.group(0)
                if sid == "hardcoded-credential" and (PLACEHOLDER.search(line) or test_file):
                    continue
                sev = "high" if sid == "hardcoded-credential" else "critical"
                self.add(f"secret:{sid}", sev, "security", f"{label} in source",
                         "Move it to an environment variable or secret manager and rotate the exposed value.",
                         rel, lineno, mask(value))
                break

            if ext in CODE_EXT:
                if not test_file and not uses_env and ENV_USAGE.search(line):
                    uses_env = True
                if not test_file:
                    if ext in JS_EXT and DEBUG_JS.search(line):
                        self.add("debug-statement", "low", "quality", "Debug statements left in code",
                                 "Remove console.log/debugger calls or route them through a real logger.", rel, lineno)
                    elif ext == ".py" and DEBUG_PY.search(line):
                        self.add("debugger-left", "medium", "quality", "Python debugger call left in code",
                                 "Remove breakpoint()/pdb calls before shipping.", rel, lineno)
                if TODO.search(line):
                    self.add("todo", "info", "quality", "TODO/FIXME markers",
                             "Review these and resolve anything that blocks launch.", rel, lineno)
                if not test_file and CORS_WILDCARD.search(line):
                    self.add("cors-wildcard", "medium", "security", "CORS allows any origin",
                             "Restrict allowed origins to your own domains.", rel, lineno)
            if ext == ".py" and "settings" in rel.lower() and DJANGO_DEBUG.search(line):
                self.add("django-debug", "high", "security", "Django DEBUG = True in settings",
                         "Read DEBUG from the environment and default it to False.", rel, lineno)

        if base.lower() == "dockerfile" or base.lower().startswith("dockerfile."):
            if not re.search(r"^\s*USER\s+(?!root\b)\S+", text, re.M | re.I):
                self.add("docker-root", "medium", "security", "Container runs as root",
                         "Add a non-root USER to the final Dockerfile stage.", rel)
            for lineno, line in enumerate(text.splitlines(), 1):
                if re.match(r"^\s*FROM\s+\S+:latest\b", line, re.I) or re.match(r"^\s*FROM\s+[^\s:@]+\s*(?:AS\s+\S+)?\s*$", line, re.I):
                    self.add("docker-unpinned", "low", "reliability", "Unpinned Docker base image",
                             "Pin base images to a specific version tag or digest.", rel, lineno)
        return uses_env

    def report(self, file_count):
        findings = sorted(self.findings.values(),
                          key=lambda f: (SEVERITY_ORDER.index(f["severity"]), f["id"]))
        score = max(0, 100 - sum(SEVERITY_WEIGHT[f["severity"]] for f in findings))
        counts = {s: sum(1 for f in findings if f["severity"] == s) for s in SEVERITY_ORDER}
        if counts["critical"]:
            verdict = "BLOCKED"
        elif counts["high"] or score < 70:
            verdict = "NOT READY"
        elif score < 90:
            verdict = "READY WITH FIXES"
        else:
            verdict = "READY"
        return {
            "tool": "ship-check", "version": VERSION, "root": self.root,
            "files_scanned": file_count, "stack": self.stack, "score": score,
            "verdict": verdict, "counts": counts, "findings": findings,
        }


def to_markdown(r):
    lines = [
        f"# Ship Check scan — {r['verdict']} ({r['score']}/100)", "",
        f"- Root: `{r['root']}`",
        f"- Files scanned: {r['files_scanned']}",
        f"- Stack: {', '.join(r['stack']) or 'unknown'}",
        "- Counts: " + ", ".join(f"{k} {v}" for k, v in r["counts"].items()), "",
    ]
    for f in r["findings"]:
        lines.append(f"## [{f['severity'].upper()}] {f['title']} ({f['count']}x)")
        lines.append(f"Fix: {f['fix']}")
        for loc in f["locations"]:
            where = loc["file"] + (f":{loc['line']}" if "line" in loc else "")
            lines.append(f"- `{where}`" + (f" — {loc['detail']}" if "detail" in loc else ""))
        lines.append("")
    return "\n".join(lines)


def main(argv=None):
    p = argparse.ArgumentParser(description="Ship Check production-readiness scanner")
    p.add_argument("path", nargs="?", default=".")
    p.add_argument("--format", choices=["json", "markdown"], default="json")
    p.add_argument("--fail-on", choices=SEVERITY_ORDER[:-1],
                   help="exit 1 if any finding at or above this severity exists (for CI)")
    p.add_argument("--version", action="version", version=f"ship-check {VERSION}")
    args = p.parse_args(argv)

    if not os.path.isdir(args.path):
        p.error(f"not a directory: {args.path}")

    result = Scanner(args.path).run()
    print(json.dumps(result, indent=2) if args.format == "json" else to_markdown(result))

    if args.fail_on:
        threshold = SEVERITY_ORDER.index(args.fail_on)
        if any(SEVERITY_ORDER.index(f["severity"]) <= threshold for f in result["findings"]):
            return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
