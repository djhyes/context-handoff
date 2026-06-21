#!/usr/bin/env python3
"""Turn a pending compact marker into one automatic continuation prompt."""

from __future__ import annotations

import json
import os
from pathlib import Path


def data_dir() -> Path:
    root = os.environ.get("PLUGIN_DATA")
    if root:
        return Path(root).expanduser()
    return Path.home() / ".codex" / "plugin-data" / "context-handoff"


def main() -> None:
    marker = data_dir() / "handoff-pending.json"
    if not marker.exists():
        print(json.dumps({"continue": True, "suppressOutput": True}))
        return

    consumed = marker.with_name("handoff-consumed.json")
    try:
        consumed.write_text(marker.read_text(encoding="utf-8"), encoding="utf-8")
        marker.unlink()
    except OSError:
        print(
            json.dumps(
                {
                    "continue": True,
                    "systemMessage": (
                        "Context Handoff saw a pending marker but could not consume it."
                    ),
                }
            )
        )
        return

    print(
        json.dumps(
            {
                "decision": "block",
                "reason": (
                    "Use $context-handoff now. Automatic compaction has occurred or "
                    "is imminent, so prepare a complete handoff document, create a "
                    "fresh Codex thread with the full handoff in its initial prompt "
                    "when thread tools are available, and stop doing feature work in "
                    "this old thread after the handoff is sent."
                ),
            }
        )
    )


if __name__ == "__main__":
    main()
