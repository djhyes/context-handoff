#!/usr/bin/env python3
"""Mark that automatic compaction happened soon enough to request handoff."""

from __future__ import annotations

import json
import os
from datetime import datetime, timezone
from pathlib import Path
from sys import stdin


def data_dir() -> Path:
    root = os.environ.get("PLUGIN_DATA")
    if root:
        return Path(root).expanduser()
    return Path.home() / ".codex" / "plugin-data" / "context-handoff"


def main() -> None:
    try:
        payload = json.load(stdin)
    except Exception:
        payload = {}

    directory = data_dir()
    directory.mkdir(parents=True, exist_ok=True)
    marker = {
        "created_at": datetime.now(timezone.utc).isoformat(),
        "trigger": payload.get("trigger", "auto"),
        "turn_id": payload.get("turn_id"),
    }
    (directory / "handoff-pending.json").write_text(
        json.dumps(marker, indent=2) + "\n",
        encoding="utf-8",
    )

    print(
        json.dumps(
            {
                "continue": True,
                "systemMessage": (
                    "Context Handoff detected automatic compaction. A follow-up "
                    "prompt will ask Codex to create a fresh-thread handoff."
                ),
            }
        )
    )


if __name__ == "__main__":
    main()
