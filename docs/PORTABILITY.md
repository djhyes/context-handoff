# Portability Guide

Context Handoff has a portable core and platform-specific adapters.

## Portable Core

These files are reusable across agents that understand Agent Skills-style folders:

- `skills/context-handoff/SKILL.md`
- `skills/context-handoff/references/handoff-template.md`
- `skills/context-handoff/references/platform-adapters.md`

The portable core teaches an agent how to produce a complete handoff and a reactivation prompt.

## Codex Adapter

Codex support lives at the repository root:

- `.codex-plugin/plugin.json`
- `hooks/hooks.json`
- `hooks/pre_compact_mark_handoff.py`
- `hooks/stop_trigger_handoff.py`

Codex is the only adapter in this repository that can currently automate the "compaction happened, now ask the model to hand off" loop using bundled plugin hooks.

## Claude Code Adapter

Claude Code can reuse the core skill format, but its hooks and invocation syntax differ:

- invoke as `/context-handoff`
- place skills under `.claude/skills/context-handoff/` or `~/.claude/skills/context-handoff/`
- configure hooks in `.claude/settings.json` or `~/.claude/settings.json`

See `adapters/claude-code/`.

## OpenClaw Adapter

OpenClaw reuse is workflow-level. Use an OpenClaw skill/prompt or cron job that asks the agent to run the handoff workflow, then sends the full handoff to a new session or back to the current channel.

See `adapters/openclaw/`.

## Hermes Adapter

Hermes reuse is bridge/runtime-level. Use the handoff workflow text, but only call Hermes session APIs after verifying they exist in the local runtime.

See `adapters/hermes/`.

## Compatibility Matrix

| Platform | Reuse `SKILL.md` | Auto compaction trigger | Auto new session | Notes |
| --- | --- | --- | --- | --- |
| Codex | Yes | Yes, with bundled hooks | Yes, when thread tools are available | Full support in this repo |
| Claude Code | Yes, with adapter copy | Partial, via Claude Code hooks | Usually manual unless a session API is available | Use `/context-handoff` |
| OpenClaw | Yes, as workflow text | Depends on OpenClaw events/cron | Depends on OpenClaw session commands | Best as persistent-agent workflow |
| Hermes | Yes, as workflow text | Runtime-specific | Runtime-specific | Verify APIs before automating |
| Generic agent | Yes, manually | No | Manual | Copy the handoff prompt |
