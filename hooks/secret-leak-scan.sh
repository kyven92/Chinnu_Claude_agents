#!/bin/bash
FILE=$(cat | jq -r '.file // empty')
if [ -n "$FILE" ] && [ -f "$FILE" ]; then
  if grep -qiE \
    '(api_key|secret|password|token|private_key)\s*[=:]\s*["\x27][a-z0-9_\-]{16,}' \
    "$FILE" 2>/dev/null; then
    echo "SECRET DETECTED in $FILE"; exit 1
  fi
fi; exit 0
