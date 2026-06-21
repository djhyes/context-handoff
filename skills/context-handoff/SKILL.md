---
name: context-handoff
description: Use automatically and immediately when an agent thread is near the context limit, automatic compaction is about to happen or just happened, the user asks to hand off/continue in a new session, or the conversation contains triggers such as context full, context almost full, compact, handoff, transfer, resume in fresh thread, 新会话, 上下文快满, 交接, 接着干, or 续上. Create a complete handoff document and start a fresh continuation thread/session when the host agent supports it.
---

# Context Handoff

Preserve continuity before the current thread becomes unreliable. The output is a complete handoff package plus, when possible, a fresh continuation thread/session that can continue the work from repo state and the handoff alone.

This skill may be invoked explicitly by the user or by the bundled auto-compact hooks. When invoked by the hook-generated prompt, treat that prompt as the user's explicit request to create a fresh continuation thread.

## Workflow

1. Stop expanding the original task. Do only the inspection needed to make the handoff accurate.
2. Load `references/handoff-template.md` before drafting the handoff.
3. Inspect current state with lightweight commands:
   - current directory and repo root
   - current branch and `git status --short --branch` when inside Git
   - changed file names and diff stats when useful
   - relevant project guidance such as `AGENTS.md`, `README`, docs, scripts, or test commands
4. Write a concise but complete handoff. Include known facts from the conversation and mark uncertain items as `Unknown` rather than inventing them.
5. Include the full handoff text in the new thread/session initial prompt. A saved file path is useful, but the continuation must not depend on reading the old chat.
6. Choose the host adapter:
   - Codex: use the Codex thread-tool workflow below.
   - Claude Code, OpenClaw, Hermes, or another agent: follow the platform notes in `references/platform-adapters.md` if this repository includes that file.
   - Unknown host: return the handoff plus a copy-paste reactivation prompt.
7. Create a fresh Codex thread when Codex thread tools are available:
   - Use `tool_search` for `create_thread`, `list_projects`, `set_thread_title`, and `send_message_to_thread` if those tools are not already visible.
   - Use `list_projects` and choose the project matching the current workspace when possible.
   - Prefer a `project` target with `environment: { "type": "local" }` so the new thread sees the same checkout and uncommitted changes.
   - Use `projectless` only when no matching project exists.
   - Do not set `model` or `thinking` unless the user explicitly requested them.
   - After creation, set a short title such as `Handoff: <goal>` when `set_thread_title` is available.
8. If thread/session tools are unavailable or policy blocks creation, provide the handoff and reactivation prompt directly in the current thread and tell the user that automatic continuation creation could not be completed.
9. After a new thread/session is created, do not continue feature work in the old thread. Finalize with the continuation status and the saved handoff location if one was written.

## Handoff Requirements

The handoff must include:

- repo/path, branch, and whether the working tree is dirty
- current goal and latest user intent
- project instructions, skills, tools, plugins, or constraints already discovered
- completed work and files touched or investigated
- commands/tests run and their outcomes
- known errors, warnings, failing checks, and environmental blockers
- open decisions, assumptions, and do-not-touch areas
- next 3-7 concrete steps in order
- exact reactivation prompt for the new thread

## New Thread Prompt

Use this structure for the initial prompt:

```text
Use $context-handoff to continue this work from a handoff.

We are continuing from a near-full Codex thread. Do not assume access to the old chat.
First read the handoff below, inspect the current repo/workspace state, verify what still applies, then continue from the listed next steps.

<full handoff document>
```

## Safety Notes

- Do not hide uncertainty. If a command result, file state, or decision is not known, say `Unknown` and give the new thread a way to verify it.
- Do not run destructive commands, broad formatting, dependency upgrades, or unrelated cleanup just to prepare a handoff.
- Do not summarize away failures; they are often the most important continuity data.
- If the context is already compacted, use the available summary and current filesystem state, then explicitly note that older transcript details may be missing.
