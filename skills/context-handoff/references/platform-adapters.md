# Platform Adapters

Use this reference when `$context-handoff` runs outside Codex or when Codex thread tools are unavailable.

## Codex

- Use `create_thread` when available.
- Put the full handoff document in the new thread's initial prompt.
- Prefer the same local project target so uncommitted changes and repo state are visible.
- Use the bundled Codex hooks only inside Codex. They are not portable to other agents.

## Claude Code

- Claude Code can use a `SKILL.md` skill, but it uses `/skill-name` invocation rather than Codex `$skill-name` invocation.
- If a new-session tool is unavailable, write the handoff and provide a prompt the user can paste into a new Claude Code session.
- Claude Code compaction hooks differ from Codex hooks. Use `SessionStart` with `matcher: "compact"` to re-inject saved handoff/context after compaction.
- Do not mention Codex-only tools such as `tool_search`, `create_thread`, or `list_projects` in the final Claude Code prompt unless the user is actually in Codex.

## OpenClaw

- Treat OpenClaw as a persistent agent with channels and scheduled jobs.
- Prefer an OpenClaw cron or channel-triggered prompt that asks the agent to run the handoff workflow.
- If OpenClaw exposes a session creation command, pass the full handoff as the first message to the new session.
- If not, send the handoff to the current channel with a clear "start new session with this prompt" block.

## Hermes

- Treat Hermes as a bridge/runtime rather than a native Codex plugin host.
- Reuse the handoff template and workflow text.
- Use Hermes session or channel APIs only when verified in the current environment.
- If Hermes lacks a reliable session creation API, publish the handoff as a channel message and tell the user how to resume from it.

## Generic Agent

When the platform is unknown:

1. Save or display the handoff.
2. Include a reactivation prompt at the top.
3. Avoid platform-specific commands.
4. Ask the user to start a fresh session with the full handoff if no session API exists.
