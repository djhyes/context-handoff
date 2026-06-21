# OpenClaw Adapter

OpenClaw can reuse Context Handoff as a persistent-agent workflow. The Codex plugin hooks do not run in OpenClaw, so use OpenClaw's own cron, channel, or session mechanism to trigger the handoff prompt.

## Skill Install Shape

Copy the portable skill into your OpenClaw/agent skills directory if your runtime scans Agent Skills-style folders:

```bash
mkdir -p ~/.agents/skills
cp -R skills/context-handoff ~/.agents/skills/context-handoff
```

If your OpenClaw setup uses a different skill directory, copy `skills/context-handoff` there instead.

## Trigger Prompt

Use this prompt from an OpenClaw channel, cron job, or session watcher:

```text
Use context-handoff. The current task may be near the context limit. Create a complete handoff document with current goal, repo/path, files touched, commands run, failures, constraints, open decisions, and next steps. If OpenClaw can create a new session, start one with the full handoff as the first message. Otherwise send the handoff and reactivation prompt back to this channel.
```

## Optional Cron Pattern

Use a conservative scheduled check rather than mutating state automatically:

```bash
openclaw cron add \
  --name "Context Handoff Check" \
  --cron "*/30 * * * *" \
  --tz "Asia/Shanghai" \
  --session isolated \
  --message "Check whether the active work needs a context handoff. If yes, use context-handoff and send the handoff to the active channel. If no, stay quiet unless the platform requires a status."
```

Adjust channel and target flags to match your OpenClaw installation.

## Boundary

OpenClaw session creation and channel routing vary by installation. Verify the exact commands in your environment before automating new-session creation.
