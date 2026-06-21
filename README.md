# Context Handoff

Context Handoff is an open-source handoff skill with a first-class Codex plugin and adapters for other agent runtimes. It preserves work when a thread is close to the context limit. It packages:

- a `$context-handoff` skill that writes a complete handoff package
- `PreCompact(auto)` and `Stop` hooks that nudge Codex to run the handoff workflow when automatic compaction happens
- a reusable handoff template for fresh continuation threads
- adapter notes for Claude Code, OpenClaw, Hermes, and generic agents

The goal is simple: before the old thread becomes unreliable, create a fresh continuation thread/session with enough context to continue without relying on the old chat transcript.

## What It Does

When triggered, the skill asks the agent to:

1. stop expanding the original task
2. inspect the current workspace lightly
3. summarize the goal, files, commands, failures, constraints, and next steps
4. include the full handoff in a new thread prompt
5. create a fresh continuation thread/session when thread-management tools are available

The Codex hook layer is intentionally narrow. It records that automatic compaction occurred, then asks Codex once to run `$context-handoff`. The model still writes the actual handoff because only the model has the conversation context.

## Platform Support

| Platform | Status | Entry point |
| --- | --- | --- |
| Codex | Full plugin support | repository root |
| Claude Code | Skill + hook adapter | `adapters/claude-code/` |
| OpenClaw | Workflow adapter | `adapters/openclaw/` |
| Hermes | Runtime/channel adapter | `adapters/hermes/` |
| Generic agents | Manual prompt reuse | `docs/PORTABILITY.md` |

See `docs/PORTABILITY.md` for the compatibility matrix and adapter boundaries.
For upgrade and stale hook cache issues, see `docs/TROUBLESHOOTING.md`.

## Install For Codex

Clone the repository:

```bash
mkdir -p ~/plugins
git clone https://github.com/djhyes/context-handoff.git ~/plugins/context-handoff
cd ~/plugins/context-handoff
```

For the standard personal marketplace layout, keep the checkout at `~/plugins/context-handoff` and add this entry to `~/.agents/plugins/marketplace.json`:

```json
{
  "name": "context-handoff",
  "source": {
    "source": "local",
    "path": "./plugins/context-handoff"
  },
  "policy": {
    "installation": "AVAILABLE",
    "authentication": "ON_INSTALL"
  },
  "category": "Productivity"
}
```

Then install it from that marketplace:

```bash
codex plugin add context-handoff@personal
```

Start a new Codex thread after installing so Codex loads the plugin and skill.

When upgrading an already-enabled plugin, reinstall and start a new thread:

```bash
codex plugin add context-handoff@personal
```

Existing threads can keep old hook file paths in memory. If an old thread reports a missing hook script from a previous version, use the stale-cache repair in `docs/TROUBLESHOOTING.md`.

## Hook Trust

Codex requires non-managed hooks to be reviewed and trusted before they run.

After installation:

1. open the hooks review UI with `/hooks` in Codex CLI, or use the Codex app hook review flow
2. review the two bundled hook scripts
3. trust the hooks
4. start a new thread to verify loading

The hooks write a small marker under `~/.codex/plugin-data/context-handoff/` by default. Set `PLUGIN_DATA` to override this location.

## Usage

Explicitly trigger the skill:

```text
Use $context-handoff to hand off this near-full thread to a fresh session.
```

Natural-language triggers also work when the skill is installed and implicitly available, for example:

```text
The context is almost full. Create a handoff and continue in a new session.
```

The new session should receive a prompt containing the full handoff document, not only a file path.

## Validation

From the plugin root:

```bash
python3 /Users/dujihui/.codex/skills/.system/skill-creator/scripts/quick_validate.py skills/context-handoff
python3 /Users/dujihui/.codex/skills/.system/plugin-creator/scripts/validate_plugin.py .
```

Smoke-test the hooks with a temporary data directory:

```bash
tmpdir="$(mktemp -d)"
printf '{"trigger":"auto","turn_id":"turn-test"}' | PLUGIN_DATA="$tmpdir" python3 hooks/pre_compact_mark_handoff.py
PLUGIN_DATA="$tmpdir" python3 hooks/stop_trigger_handoff.py
PLUGIN_DATA="$tmpdir" python3 hooks/stop_trigger_handoff.py
```

The second `stop_trigger_handoff.py` call should be quiet because the marker is consumed once.

## Known Boundaries

- A skill is not a background daemon.
- Hooks can detect automatic compaction in supported hosts, but shell hooks cannot themselves write a high-quality conversation handoff.
- Fresh thread creation depends on whether the current Codex environment exposes thread tools such as `create_thread`.
- If thread creation is unavailable, the skill should still return a handoff and reactivation prompt in the current thread.

## License

MIT
