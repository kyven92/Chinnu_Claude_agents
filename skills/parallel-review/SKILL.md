---
name: parallel-review
description: >
  Dispatch code-reviewer, test-runner, and docs-checker simultaneously
  on the current session's changes. More thorough than single-agent review.
  Use after a significant block of implementation work.
user-invocable: true
allowed-tools: Read, Bash
---

# Parallel Review

Dispatch three review tasks simultaneously against the current branch diff.

## Step 1 — Get changed files

```bash
git diff --name-only main...HEAD 2>/dev/null || git diff --name-only HEAD~1
```

## Step 2 — Dispatch simultaneously

Issue all three tasks in one message to run in parallel:

"Do all three simultaneously:

1. [chinnu-code-reviewer]: Review the diff on the current branch against main.
   Check: code quality, spec compliance, naming, error handling.
   Output: numbered findings by severity.

2. [test-runner (using Bash tool)]: Run the full test suite and coverage report.
   Show: pass/fail counts, coverage %, any failing test names.

3. [build-error-resolver (read-only check)]: Check that the build passes cleanly.
   Run: the project's build command (npm run build / go build / python -m py_compile).
   Output: PASS or list of errors."

## Step 3 — Consolidate results

After all three complete, print a combined summary:
```
Parallel Review Results
──────────────────────
Code Review:  {n findings: X HIGH, Y MED, Z LOW}
Tests:        {PASSING / FAILING — n failures} | Coverage: {n}%
Build:        {PASS / FAIL}

Verdict: {READY TO SHIP / FIXES NEEDED}
```

If any BLOCK_MERGE findings or failing tests: list what must be fixed first.
