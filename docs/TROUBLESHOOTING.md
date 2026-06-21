# Troubleshooting

## Old Thread Reports A Missing Hook Script

Symptom:

```text
can't open file '/Users/.../.codex/plugins/cache/personal/context-handoff/0.1.0/hooks/stop_trigger_handoff.py': [Errno 2] No such file or directory
```

Cause:

An existing Codex thread loaded hook file paths from an older plugin cache version. After the plugin was upgraded, Codex installed the new version, but the already-open thread may still try to run the old absolute hook path. New threads should load the current version.

First verify the installed version:

```bash
codex plugin list | sed -n '1,20p'
```

Then reinstall the plugin and start a new thread:

```bash
codex plugin add context-handoff@personal
```

If you must keep using the already-open old thread, run the bundled repair script from the plugin checkout. Pass the stale versions shown in hook errors:

```bash
python3 scripts/repair_stale_hook_cache.py 0.1.0 0.2.0
```

Smoke-test the shim:

```bash
tmpdir="$(mktemp -d)"
old="$HOME/.codex/plugins/cache/personal/context-handoff/0.2.0/hooks"
printf '{"trigger":"auto","turn_id":"shim-test"}' | PLUGIN_DATA="$tmpdir" python3 "$old/pre_compact_mark_handoff.py"
PLUGIN_DATA="$tmpdir" python3 "$old/stop_trigger_handoff.py"
PLUGIN_DATA="$tmpdir" python3 "$old/stop_trigger_handoff.py"
```

The second stop call should be quiet because the marker is consumed once.

## Hook Needs Review Again

Codex requires non-managed hooks to be trusted. If `/hooks` reports that Context Handoff hooks changed after an upgrade, review and trust them again.

## Hook Runs But No New Thread Is Created

The hook only asks the model to run `$context-handoff`. New thread creation still depends on whether the current Codex environment exposes thread tools such as `create_thread`. If those tools are unavailable, the skill should return a handoff and reactivation prompt in the current thread.
