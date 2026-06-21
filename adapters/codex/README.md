# Codex Adapter

The Codex adapter is implemented at the repository root so the checkout itself remains an installable Codex plugin.

Relevant files:

- `.codex-plugin/plugin.json`
- `skills/context-handoff/SKILL.md`
- `hooks/hooks.json`
- `hooks/pre_compact_mark_handoff.py`
- `hooks/stop_trigger_handoff.py`

Install through a Codex marketplace entry that points at the repository root. See the root `README.md` for the full install flow.

Codex is currently the most complete adapter because it can combine the portable skill with plugin-bundled `PreCompact(auto)` and `Stop` hooks plus Codex app thread tools.

## Upgrade Note

Codex threads load plugin hook file paths when the thread starts. After upgrading the plugin, start a new thread so it loads the latest cached version. If an already-open thread reports a missing hook script from an older cache path, follow `docs/TROUBLESHOOTING.md`.
