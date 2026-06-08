#!/usr/bin/env bash
set -euo pipefail
out="ALL_Skills.md"
{
  echo "## HOW TO INSTALL THESE SKILLS"
  echo "## Save each block as: ~/.claude/skills/{skill-name}/SKILL.md"
  echo "## After saving: restart Claude Code or wait for live reload"
  echo
  i=0
  for dir in skills/*/; do
    i=$((i+1))
    name=$(basename "$dir")
    echo
    echo "# ════════════════════════════════════════════════════════"
    echo "# SKILL ${i}: ${name}"
    echo "# Path: ~/.claude/skills/${name}/SKILL.md"
    echo "# Invoke: /${name}"
    echo "# ════════════════════════════════════════════════════════"
    echo
    cat "${dir}SKILL.md"
    echo
  done
} > "$out"
echo "Wrote $out"
