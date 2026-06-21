#!/usr/bin/env python3
"""Create compatibility shims for stale context-handoff Codex hook cache paths."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


HOOKS_JSON = {
    "hooks": {
        "PreCompact": [
            {
                "matcher": "auto",
                "hooks": [
                    {
                        "type": "command",
                        "command": "python3 ${PLUGIN_ROOT}/hooks/pre_compact_mark_handoff.py",
                        "statusMessage": "Preparing a context handoff marker",
                    }
                ],
            }
        ],
        "Stop": [
            {
                "hooks": [
                    {
                        "type": "command",
                        "command": "python3 ${PLUGIN_ROOT}/hooks/stop_trigger_handoff.py",
                        "statusMessage": "Checking whether a context handoff is pending",
                        "timeout": 30,
                    }
                ]
            }
        ],
    }
}


SHIM_TEMPLATE = '''#!/usr/bin/env python3
"""Compatibility shim for threads that loaded stale context-handoff hooks."""

from __future__ import annotations

import runpy
from pathlib import Path


def latest_script(name: str) -> Path:
    cache_root = Path.home() / ".codex" / "plugins" / "cache" / "personal" / "context-handoff"
    current_file = Path(__file__).resolve()
    candidates = [
        path
        for path in cache_root.glob("*/hooks/" + name)
        if path.resolve() != current_file and "Compatibility shim" not in path.read_text(encoding="utf-8", errors="ignore")[:300]
    ]
    if candidates:
        return sorted(candidates)[-1]
    return Path.home() / "plugins" / "context-handoff" / "hooks" / name


runpy.run_path(str(latest_script("{script_name}")), run_name="__main__")
'''


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Repair stale context-handoff hook paths held by already-open Codex threads."
    )
    parser.add_argument(
        "versions",
        nargs="*",
        help="Old cache versions to repair, such as 0.1.0 0.2.0. Defaults to all missing common versions.",
    )
    parser.add_argument(
        "--cache-root",
        default=str(Path.home() / ".codex" / "plugins" / "cache" / "personal" / "context-handoff"),
        help="context-handoff plugin cache root.",
    )
    return parser.parse_args()


def write_shim(hooks_dir: Path, script_name: str) -> None:
    path = hooks_dir / script_name
    path.write_text(SHIM_TEMPLATE.format(script_name=script_name), encoding="utf-8")
    path.chmod(0o755)


def main() -> None:
    args = parse_args()
    cache_root = Path(args.cache_root).expanduser()
    installed_versions = sorted(path.name for path in cache_root.iterdir() if path.is_dir()) if cache_root.exists() else []
    latest = installed_versions[-1] if installed_versions else None
    versions = args.versions or ["0.1.0", "0.2.0"]

    repaired: list[str] = []
    for version in versions:
        if latest is not None and version == latest:
            continue
        hooks_dir = cache_root / version / "hooks"
        hooks_dir.mkdir(parents=True, exist_ok=True)
        write_shim(hooks_dir, "pre_compact_mark_handoff.py")
        write_shim(hooks_dir, "stop_trigger_handoff.py")
        (hooks_dir / "hooks.json").write_text(json.dumps(HOOKS_JSON, indent=2) + "\n", encoding="utf-8")
        repaired.append(str(hooks_dir))

    print(json.dumps({"cache_root": str(cache_root), "latest": latest, "repaired": repaired}, indent=2))


if __name__ == "__main__":
    main()
