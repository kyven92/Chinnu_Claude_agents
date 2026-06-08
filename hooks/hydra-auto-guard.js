#!/usr/bin/env node

// Hydra Auto-Guard Hook — PostToolUse (matcher: Agent)
// Fires only when a chinnu-* subagent completes.
// Sets sentinel-pending flag and emits a dispatch directive.

const fs = require('fs');
const path = require('path');
const os = require('os');

let input = '';
process.stdin.on('data', (chunk) => (input += chunk));
process.stdin.on('end', () => {
  try {
    const data = JSON.parse(input);

    // Only act on chinnu agents
    const subagentType = data.tool_input?.subagent_type || '';
    if (!subagentType.startsWith('chinnu-')) {
      process.exit(0);
    }

    const sessionId = data.session_id || 'unknown';

    // === Sentinel Pending Flag ===
    const sentinelDir = path.join(os.tmpdir(), 'hydra-sentinel');
    const sentinelFlag = path.join(sentinelDir, `${sessionId}-pending.json`);

    if (!fs.existsSync(sentinelDir)) {
      fs.mkdirSync(sentinelDir, { recursive: true });
    }

    let pending = { agent: subagentType, created_at: Date.now() };
    try {
      pending = JSON.parse(fs.readFileSync(sentinelFlag, 'utf8'));
    } catch (e) { /* new flag */ }

    pending.agent = subagentType;
    pending.updated_at = Date.now();
    fs.writeFileSync(sentinelFlag, JSON.stringify(pending));

    // Invalidate any prior clean marker
    try {
      const scanMarker = path.join(sentinelDir, `${sessionId}-last-scan`);
      if (fs.existsSync(scanMarker)) fs.unlinkSync(scanMarker);
    } catch (_) { /* silent */ }

    // Emit directive to dispatch sentinel scan
    const directive = {
      hookSpecificOutput: {
        hookEventName: 'PostToolUse',
        additionalContext: `🐉 Hydra Auto-Guard: ${subagentType} agent completed. Dispatch hydra-sentinel-scan to verify integration before presenting results to the user.`
      }
    };

    process.stdout.write(JSON.stringify(directive));

  } catch (e) {
    // Silently fail — NEVER block Claude Code
  }
  process.exit(0);
});
