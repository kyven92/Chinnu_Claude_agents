#!/bin/bash
# Prevents agent identity drift after context compression
[ -f ~/.claude/identity-core.md ] && cat ~/.claude/identity-core.md
exit 0
# identity-core.md = 50-token condensed version of your CLAUDE.md hard rules
