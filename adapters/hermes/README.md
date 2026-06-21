# Hermes Adapter

Hermes can reuse Context Handoff as a runtime/channel workflow. Hermes does not load Codex plugin manifests or Codex hooks, so treat this adapter as prompt and integration guidance.

## Reuse Pattern

1. Copy or expose `skills/context-handoff/SKILL.md` and its `references/` files to the Hermes agent prompt/skill path.
2. Trigger the handoff prompt when a long-running Hermes session approaches its context limit or when the user asks to continue elsewhere.
3. If Hermes exposes a verified session creation API, send the full handoff as the first message to the new session.
4. If no session API exists, send the handoff and reactivation prompt back through the current channel.

## Trigger Prompt

```text
Use context-handoff. Prepare a complete handoff for this Hermes agent session. Include current goal, environment, files/tools touched, commands run, failures, constraints, open decisions, and next steps. If a verified Hermes session API is available, create a new session with the full handoff. Otherwise return the full handoff and reactivation prompt in this channel.
```

## Boundary

Do not assume Hermes has Codex-style `create_thread` tools. Verify local Hermes commands, gateway state, and session API before attempting automatic continuation.
