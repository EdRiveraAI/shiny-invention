# Ship Check

**Know whether your app is ready to launch, in five minutes.**

Ship Check is an AI agent skill for **Claude Code** and **OpenAI Codex**. Ask your agent
"is this ready to ship?" and you get a scored production-readiness and security audit of your
repository, with a clear verdict and file-specific fixes in priority order.

```
Ship Check: acme-api
Verdict: NOT READY · Score: 61/100
Stack: Node.js, Docker

Fix these first
1. Stripe live key in source (critical) — src/billing.js:12. Anyone with repo access can charge
   cards. Fix: rotate the key, load it from STRIPE_SECRET_KEY.
2. /invoices/:id has no ownership check (critical) — src/routes/invoices.js:40 ...
3. No timeouts on outbound HTTP calls (high) — src/lib/http.js:8 ...
```

## What it checks

- **Automated scan** (bundled, dependency-free Python script): leaked secrets and API keys
  (AWS, Stripe, GitHub, Slack, Google, OpenAI, Anthropic, private keys, hard-coded passwords),
  committed `.env` files, `.gitignore` gaps, missing tests/CI/lockfiles/`.env.example`, debug
  statements, CORS wildcards, Django `DEBUG=True`, Dockerfiles running as root or unpinned,
  oversized files.
- **Guided expert review** (by your agent, using a 60+ point checklist): authentication and
  authorization, IDOR, injection, XSS, CSRF, SSRF, file uploads, webhook signatures, password
  hashing, rate limiting, error handling, logging, monitoring, timeouts, N+1 queries, backups,
  migrations, deployment and rollback, plus stack-specific checks for Node/Express, Next.js,
  Django, Flask/FastAPI, Rails, Go, Docker, and Terraform.
- **Verified findings only**: the agent confirms every automated hit in the code and drops
  false positives before reporting.
- **Fix mode**: after the report, the agent offers to fix issues one by one and re-scores.
- **CI mode**: run the scanner in your pipeline and fail builds on high or critical issues.

Secrets are always masked in the output. Nothing is changed in your repo until you approve it.

## Requirements

- Claude Code or OpenAI Codex (any version with Agent Skills support)
- Python 3.8+ (standard library only, no `pip install` needed)
- macOS, Linux, or Windows (WSL or Git Bash for the installer)

## Install

Unzip the package, then:

```bash
./install.sh            # auto-detects Claude Code and/or Codex
./install.sh --all      # install for both
./install.sh --project /path/to/repo   # share with your team via the repo
```

| Tool | Installs to | Run it |
|---|---|---|
| Claude Code | `~/.claude/skills/ship-check/` | `/ship-check` or "is this ready to ship?" |
| Codex | `~/.agents/skills/ship-check/` | `$ship-check` or "is this ready to ship?" |

**Manual install:** copy the `skills/ship-check` folder into the directory above for your tool.
For older Codex versions that read `~/.codex/skills`, run
`CODEX_SKILLS_DIR=~/.codex/skills ./install.sh --codex`.

**As a Claude Code plugin:** this package also contains `.claude-plugin/plugin.json`, so it can
be added to a private plugin marketplace for team distribution.

**Uninstall:** `./install.sh --all --uninstall`

## CI usage

```yaml
# .github/workflows/ship-check.yml
name: ship-check
on: [push, pull_request]
jobs:
  scan:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: python3 tools/ship-check/scan.py . --format markdown --fail-on high
```

Copy `skills/ship-check/scripts/scan.py` into your repo (for example `tools/ship-check/`) first.
Your license covers this use within your organization.

## Support and updates

- Updates: free for 12 months from purchase; download the latest version from your purchase
  receipt link.
- Support: support@example.com (reply within 2 business days).

## License

Commercial software. See [LICENSE.md](LICENSE.md).
