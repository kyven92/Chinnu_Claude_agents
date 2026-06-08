---
name: ship-feature
description: >
  Finish and ship a completed feature branch. Runs the full
  test suite, triggers deep code review, then presents options
  to merge, open a PR, or keep the branch.
  Run when implementation is complete and you're ready to ship.
  Arguments: optional branch name (defaults to current branch)
user-invocable: true
argument-hint: "[branch-name, defaults to current]"
allowed-tools: Read, Bash, Glob, Grep
---

# Ship Feature

Run the pre-ship checklist then hand off to finishing-a-development-branch.

## Step 1 — Confirm branch

```bash
BRANCH=$(git branch --show-current)
echo "Current branch: $BRANCH"
```

If argument passed, checkout that branch first:
```bash
git checkout {argument}
```

## Step 2 — Run full test suite

```bash
# Detect test runner
if [ -f "package.json" ]; then
  npm test 2>&1 | tail -30
elif [ -f "pyproject.toml" ] || [ -f "setup.py" ]; then
  python -m pytest --tb=short 2>&1 | tail -30
elif [ -f "go.mod" ]; then
  go test ./... 2>&1 | tail -30
fi
```

If tests fail: STOP. Report failures. Do not proceed.
```
❌ Tests failing — cannot ship.
   Fix these before running /ship-feature again:
   {test failure summary}
```

## Step 3 — Run coverage check

```bash
# TypeScript/JS
npx jest --coverage --coverageReporters=text-summary 2>/dev/null | grep "All files"
# Python
python -m pytest --cov --cov-report=term-missing 2>/dev/null | tail -5
# Go  
go test -cover ./... 2>/dev/null | grep -E "coverage|ok"
```

If coverage below 80%: warn but don't block (blocking is implementer's job):
```
⚠️  Coverage: {n}% — below 80% target
    Consider adding tests before shipping.
    Continue anyway? [y/n]
```

## Step 4 — Run Layer 2 deep code review

Invoke the chinnu-code-reviewer agent on the full branch diff:
"Review the diff between main and {branch}. 
Check: spec compliance, code quality, security basics.
Output: numbered findings by severity. State verdict: APPROVE or REQUEST CHANGES."

If code-reviewer outputs BLOCK_MERGE: STOP and show the HIGH findings.

## Step 5 — Present ship options

```
✅ Pre-ship checklist complete
   Branch: {branch}
   Tests: PASSING
   Coverage: {n}%
   Code review: {APPROVED / n findings}

   How would you like to ship?
   [1] Merge to main now
   [2] Open a draft PR
   [3] Open a ready PR
   [4] Keep branch, ship later
   [5] Discard branch and worktree
```

Wait for user choice, then execute.

For options 1-3, run:
```bash
# Option 1: merge
git checkout main && git merge {branch} && git push

# Option 2: draft PR (requires gh CLI)
gh pr create --draft --title "{branch}" --body "Closes #{issue}"

# Option 3: ready PR
gh pr create --title "{branch}" --body "Closes #{issue}"
```

## Step 6 — Clean up worktree if used

```bash
# Check if branch has a worktree
git worktree list | grep {branch}
# If yes, remove it:
git worktree remove {worktree-path}
```

## Step 7 — Prompt session-end

```
Feature shipped ✅
Run /session-end to save session notes before closing.
```
