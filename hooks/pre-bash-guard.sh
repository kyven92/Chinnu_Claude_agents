#!/bin/bash
PAYLOAD=$(cat)
CMD=$(echo "$PAYLOAD" | jq -r '.input.command // empty')
BLOCKED=("rm -rf /" "curl | sh" "wget | bash" "sudo rm" "> /dev/sd" "eval \$(")
for p in "${BLOCKED[@]}"; do
  if echo "$CMD" | grep -qF "$p"; then
    echo "BLOCKED: $p"; exit 1
  fi
done; exit 0
