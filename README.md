# Context Handoff

Context Handoff is a local Codex plugin that preserves work when a thread is close to the context limit. It packages:

- a `$context-handoff` skill that writes a complete handoff package
- `PreCompact(auto)` and `Stop` hooks that nudge Codex to run the handoff workflow when automatic compaction happens
- a reusable handoff template for fresh continuation threads

The goal is simple: before the old thread becomes unreliable, create a fresh Codex thread with enough context to continue without relying on the old chat transcript.

## What It Does

When triggered, the skill asks Codex to:

1. stop expanding the original task
2. inspect the current workspace lightly
3. summarize the goal, files, commands, failures, constraints, and next steps
4. include the full handoff in a new thread prompt
5. create a fresh Codex thread when thread-management tools are available

The hook layer is intentionally narrow. It records that automatic compaction occurred, then asks Codex once to run `$context-handoff`. The model still writes the actual handoff because only the model has the conversation context.

## Install From This Repository

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

- A Codex skill is not a background daemon.
- Hooks can detect automatic compaction, but shell hooks cannot themselves write a high-quality conversation handoff.
- Fresh thread creation depends on whether the current Codex environment exposes thread tools such as `create_thread`.
- If thread creation is unavailable, the skill should still return a handoff and reactivation prompt in the current thread.

## License

MIT
