Now I have everything I need. Let me build a comprehensive, well-structured reference artifact.Here's your complete Claude Code setup guide. Here's a summary of what's covered and the key insights from the research:

---

## 🏆 Top Insights to Act On First

**1. CLAUDE.md is your most leveraged file.** The single most expensive mistake is letting Claude start coding before you've agreed on what to build — and your CLAUDE.md structure is the fix. Put the most important rules first; Claude pays more attention to content near the top. Keep it under 500 tokens — a 5,000-token CLAUDE.md costs 5,000 tokens before you've typed a word, every turn, every session.

**2. Always start in Plan Mode.** Boris Cherny's (Claude Code's creator) team always starts in Plan Mode — have one Claude draft the plan, then a second one review it "as a staff engineer," and only then move to execution.

**3. Subagents are your most token-efficient tool.** Subagents run within a parent session and report results back, making them the most token-efficient agent type. When a subagent processes a task, all verbose intermediate work stays inside the subagent's context — only the summary returns to the parent. Your main conversation stays clean and focused.

**4. Hooks are your strongest guardrail.** The strongest guardrails live outside the model: small scripts, narrow matchers, explicit exit codes, and reviewable settings — not just soft instructions. Use `PreToolUse` to block dangerous commands before execution and `PostToolUse` to auto-format/lint after file writes.

**5. For heavy multi-agent orchestration, Ruflo is the community standard.** Ruflo has over 31,100 stars on GitHub, is used by dozens of enterprise teams, and claims 84.8% solve rate on SWE-bench with 75% API cost savings compared to using Claude Code directly.

**6. Keep agent teams small.** Each teammate runs its own context window, so token usage is roughly proportional to team size. Keep spawn prompts focused, and clean up teams when work is done — active teammates continue consuming tokens even if idle.

The artifact has 8 tabs covering every area — click through **Installation → CLAUDE.md → Code Generation → Code Review → Security → Multi-Agent → Token Efficiency → Resources** with copy-paste ready configs for all of them.