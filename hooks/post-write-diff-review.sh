#!/bin/bash
FILE=$(cat | jq -r '.file // empty')
if [[ "$FILE" =~ \.(ts|py|go|rs|js|tsx|jsx)$ ]]; then
  echo '{"invoke_agent":"code-reviewer",
         "context":"Layer 1 diff review on '"$FILE"'"}'
fi; exit 0
