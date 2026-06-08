---
name: security-review
description: >
  Invoke the chinnu-security-auditor agent on auth code, payment flows,
  user data handling, or external API integrations.
  Use before merging any feature that touches sensitive code.
  Arguments: optional path or feature name to scope the review.
  Example: /security-review src/auth/ or /security-review "OAuth feature"
user-invocable: true
argument-hint: "[path or feature description]"
allowed-tools: Read, Bash, Glob, Grep
---

# Security Review

Invoke the chinnu-security-auditor agent on the specified scope.

## Step 1 — Determine scope

If the user passed an argument, use that as the scope.
If no argument, determine scope automatically:
```bash
git diff --name-only HEAD~1  # files changed in last commit
git diff --name-only         # uncommitted changed files
```

Filter to security-sensitive files:
- Auth: anything matching `*auth*`, `*login*`, `*session*`, `*token*`, `*oauth*`
- Payments: anything matching `*payment*`, `*stripe*`, `*billing*`
- User data: anything matching `*user*`, `*profile*`, `*pii*`
- APIs: anything matching `*api*`, `*webhook*`, `*external*`

## Step 2 — Report scope to user and confirm

```
🔒 Security review scope:
   {list of files or feature description}

   This will invoke the chinnu-security-auditor agent (Opus, forked context).
   Estimated time: 2-5 minutes.
   Proceed? [y/n]
```

Wait for confirmation before invoking.

## Step 3 — Invoke security-auditor

Pass the scope to the chinnu-security-auditor agent with this prompt:

"Security audit the following files/feature: {scope}

Use your loaded Trail of Bits skills:
- audit-context-building: read and understand the code first
- static-analysis: check for injection, auth bypass, data exposure  
- insecure-defaults: check for insecure configuration
- variant-analysis: if you find a vulnerability, search the whole
  codebase for the same pattern

Output findings in SARIF format:
[CWE-{id}] {SEVERITY} | {file}:{line} | {description} | {remediation}

After findings: state overall verdict — SAFE / NEEDS FIXES / CRITICAL"

## Step 4 — Surface findings to user

After the agent completes, show the verdict and findings summary.
If CRITICAL findings: recommend blocking merge.
If NEEDS FIXES: list fixes required before merge.
If SAFE: confirm the review passed.
