# Claude Code Adapter

Claude Code can reuse Context Handoff as a filesystem skill.

## Install

For a user-wide install:

```bash
mkdir -p ~/.claude/skills
cp -R skills/context-handoff ~/.claude/skills/context-handoff
```

For a project-local install:

```bash
mkdir -p .claude/skills
cp -R skills/context-handoff .claude/skills/context-handoff
```

Invoke it in Claude Code with:

```text
/context-handoff
```

or ask naturally:

```text
The context is almost full. Create a handoff so I can continue in a fresh Claude Code session.
```

## Optional Compaction Hook

Claude Code hooks are not the same as Codex hooks. Use `SessionStart` with `matcher: "compact"` to re-inject saved handoff/context after compaction.

Copy the example:

```bash
mkdir -p .claude/hooks
cp adapters/claude-code/context-handoff-reminder.sh .claude/hooks/context-handoff-reminder.sh
chmod +x .claude/hooks/context-handoff-reminder.sh
```

Then merge `settings.example.json` into `.claude/settings.json`.

## Boundary

This adapter does not automatically create a new Claude Code session. If your Claude Code environment exposes a session API, wire it into the handoff workflow; otherwise the skill returns a reactivation prompt for manual use.
