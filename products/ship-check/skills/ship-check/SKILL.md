---
name: ship-check
description: Production-readiness and security audit for a codebase. Use when the user asks if their app is ready to ship, launch, deploy or go to production, wants a pre-launch checklist, a security review of the whole repo, a "launch audit", or asks what to fix before going live. Produces a scored report (0-100) with a verdict and prioritized, file-specific fixes.
license: Commercial. See LICENSE.md in the distribution.
metadata:
  version: "1.0.0"
---

# Ship Check

Audit the current repository for production readiness and deliver a scored, prioritized
report the user can act on immediately. Work in four phases and do not skip any.

## Ground rules

- **Never print a full secret.** Quote only masked values (the scanner masks them for you).
- **Read-only until approved.** Do not edit, delete, commit, or rotate anything until the user
  says which fixes to apply.
- **Verify before reporting.** Every finding in the final report must be something you
  confirmed by looking at the code. Drop false positives and say how many you dropped.
- **Be specific.** Every finding names the file (and line when possible), the risk in one
  sentence, and the concrete fix.

## Phase 1 — Automated scan

Run the bundled scanner from the repository root. The script lives in `scripts/scan.py`
next to this SKILL.md file; resolve that path from this skill's directory.

```bash
python3 <this-skill-dir>/scripts/scan.py . --format json
```

- It needs only Python 3.8+ and the standard library. If `python3` is missing, try `python`.
- If it cannot run at all, tell the user and continue with Phases 2–4 manually.
- Keep the JSON: `stack`, `score`, `verdict`, `counts`, and `findings`.

## Phase 2 — Verify the scan findings

For each finding in the JSON, open the referenced locations and decide:

- **Confirmed** — keep it, with the scanner's severity unless context clearly changes it.
- **False positive** — e.g. a test fixture, a documented placeholder, a value that is clearly
  public (a publishable key). Drop it and count it.

Secrets deserve extra care: if a real secret is confirmed, it is compromised the moment it was
committed. The fix is always *rotate* first, then remove from code and history.

## Phase 3 — Manual review

The scanner only catches patterns. Now review what it cannot see. Read
`references/checklist.md` and work through the sections that apply to the detected `stack`.
Prioritize, in this order:

1. Authentication and authorization (who can reach which data)
2. Input handling (injection, unsafe deserialization, file uploads, SSRF)
3. Secrets and configuration (prod vs. dev settings)
4. Data safety (migrations, backups, destructive operations)
5. Error handling, logging, and observability
6. Performance and reliability (timeouts, retries, N+1 queries, unbounded work)
7. Deployment, docs, and operations

Sample intelligently on large repos: entry points, routes/controllers, auth middleware,
database access, payment and webhook handlers, and config files first. State in the report
which areas you reviewed and which you did not reach.

Assign manual findings a severity with these definitions:

| Severity | Meaning |
|---|---|
| critical | Exploitable now or causes data loss/leak. Blocks launch. |
| high | Likely to cause an incident or security issue soon after launch. Fix before launch. |
| medium | Real risk or operational pain. Fix within the first weeks. |
| low | Hygiene and polish. |
| info | Worth knowing; no action required. |

## Phase 4 — Report

Write the report using `references/report-template.md`. Recompute the final score from the
verified findings (critical −25, high −10, medium −4, low −1; one deduction per distinct
issue; floor 0) and derive the verdict:

- **BLOCKED** — any critical finding
- **NOT READY** — any high finding, or score below 70
- **READY WITH FIXES** — score 70–89
- **READY** — score 90+

Show the report in the conversation. If the user asks for a file, save it as
`SHIP_CHECK_REPORT.md` in the repo root.

End by offering to fix the issues, starting with the top three, and ask which ones to apply.
When fixing, make one focused change per issue and re-run the scanner afterwards to show the
score change.

## CI mode

If the user wants this enforced in CI, suggest adding a step that runs:

```bash
python3 path/to/scan.py . --format markdown --fail-on high
```

It exits with status 1 when any finding at or above the chosen severity exists.
