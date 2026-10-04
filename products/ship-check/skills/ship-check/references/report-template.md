# Ship Check report template

Fill in every section. Keep it scannable: the user should know within ten seconds whether they
can ship and what to do first.

---

# Ship Check: <project name>

**Verdict: <BLOCKED | NOT READY | READY WITH FIXES | READY>** · **Score: <n>/100**
Stack: <detected stack> · Files scanned: <n> · Date: <YYYY-MM-DD>

## Fix these first

1. **<Title>** (<severity>) — `<file>:<line>`. <One-sentence risk.> **Fix:** <concrete action>.
2. ...
3. ...

## All findings

| # | Severity | Category | Finding | Location | Fix |
|---|---|---|---|---|---|
| 1 | critical | security | ... | `path:line` | ... |

## What looks good

- <2–5 genuine strengths, e.g. "All DB access goes through the ORM with parameterized queries.">

## Coverage

- Reviewed: <areas and key files actually read>
- Not reviewed: <areas skipped or out of reach>
- Scanner findings dropped as false positives: <n> (<one-line reason each>)

## Next steps

Ask which fixes to apply. Suggest starting with the "Fix these first" list, then re-running
Ship Check to confirm the new score.
