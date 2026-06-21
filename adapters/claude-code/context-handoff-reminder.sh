#!/usr/bin/env bash
set -euo pipefail

handoff_file="${CLAUDE_PROJECT_DIR:-$PWD}/.claude/context-handoff-latest.md"

if [[ -f "$handoff_file" ]]; then
  echo "Context Handoff reminder: a previous handoff exists at $handoff_file."
  echo "Read it before continuing, verify the current repo state, then continue from its next steps."
else
  echo "Context Handoff reminder: after compaction, consider running /context-handoff if important task details may have been lost."
fi
