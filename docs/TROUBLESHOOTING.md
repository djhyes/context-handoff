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

If you must keep using the already-open old thread, create a local compatibility shim from the missing old cache path to the current installed script. Replace `0.1.0` and `0.2.1` with the versions shown in your error and plugin list:

```bash
old="$HOME/.codex/plugins/cache/personal/context-handoff/0.1.0/hooks"
new="$HOME/.codex/plugins/cache/personal/context-handoff/0.2.1/hooks"
mkdir -p "$old"

cat > "$old/stop_trigger_handoff.py" <<'PY'
#!/usr/bin/env python3
from __future__ import annotations

import runpy
from pathlib import Path

current = sorted(
    (Path.home() / ".codex/plugins/cache/personal/context-handoff").glob("*/hooks/stop_trigger_handoff.py")
)
target = current[-1] if current else Path.home() / "plugins/context-handoff/hooks/stop_trigger_handoff.py"
runpy.run_path(str(target), run_name="__main__")
PY

cat > "$old/pre_compact_mark_handoff.py" <<'PY'
#!/usr/bin/env python3
from __future__ import annotations

import runpy
from pathlib import Path

current = sorted(
    (Path.home() / ".codex/plugins/cache/personal/context-handoff").glob("*/hooks/pre_compact_mark_handoff.py")
)
target = current[-1] if current else Path.home() / "plugins/context-handoff/hooks/pre_compact_mark_handoff.py"
runpy.run_path(str(target), run_name="__main__")
PY
```

Smoke-test the shim:

```bash
tmpdir="$(mktemp -d)"
printf '{"trigger":"auto","turn_id":"shim-test"}' | PLUGIN_DATA="$tmpdir" python3 "$old/pre_compact_mark_handoff.py"
PLUGIN_DATA="$tmpdir" python3 "$old/stop_trigger_handoff.py"
PLUGIN_DATA="$tmpdir" python3 "$old/stop_trigger_handoff.py"
```

The second stop call should be quiet because the marker is consumed once.

## Hook Needs Review Again

Codex requires non-managed hooks to be trusted. If `/hooks` reports that Context Handoff hooks changed after an upgrade, review and trust them again.

## Hook Runs But No New Thread Is Created

The hook only asks the model to run `$context-handoff`. New thread creation still depends on whether the current Codex environment exposes thread tools such as `create_thread`. If those tools are unavailable, the skill should return a handoff and reactivation prompt in the current thread.
