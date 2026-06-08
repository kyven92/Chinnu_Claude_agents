#!/usr/bin/env bash
# Verify that skills/, agents/, and ALL_Skills.md stay in sync with the HTML guide.
# Exits 1 on any drift, 0 when everything matches.
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
HTML="$REPO_ROOT/claude_code_master_guide.html"
cd "$REPO_ROOT"

err=0

# Check 1: every skills/* directory is referenced in the HTML guide
for dir in "$REPO_ROOT"/skills/*/; do
  name=$(basename "$dir")
  if ! grep -q "/${name}" "$HTML"; then
    echo "DRIFT: skill '${name}' not referenced in claude_code_master_guide.html"
    err=1
  fi
done

# Check 2: every agents/*.md file is referenced in the HTML guide
for f in "$REPO_ROOT"/agents/*.md; do
  name=$(basename "$f" .md)
  if ! grep -q "${name}\.md" "$HTML"; then
    echo "DRIFT: agent '${name}' not referenced in claude_code_master_guide.html"
    err=1
  fi
done

# Check 3: ALL_Skills.md matches regen from skills/
tmp=$(mktemp)
cp "$REPO_ROOT/ALL_Skills.md" "$tmp"
"$REPO_ROOT/scripts/build-all-skills.sh" > /dev/null
if ! diff -q "$tmp" "$REPO_ROOT/ALL_Skills.md" > /dev/null 2>&1; then
  echo "DRIFT: ALL_Skills.md does not match regen from skills/"
  err=1
fi
cp "$tmp" "$REPO_ROOT/ALL_Skills.md"
rm -f "$tmp"

if [ "$err" -eq 0 ]; then
  echo "OK: guide, skills, agents, and ALL_Skills.md are in sync."
fi

exit $err
