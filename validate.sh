#!/usr/bin/env bash
# Validates all workflow.json files meet repository requirements.
# Usage: bash validate.sh
# Exit 0 = all pass. Exit 1 = failures found.
#
# Thin wrapper — the actual checks live in scripts/validate.py (one JSON
# parse per file, full convention coverage per CLAUDE.md). Kept as a shell
# entrypoint so `bash validate.sh` keeps working exactly as documented.
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
exec python3 "$SCRIPT_DIR/scripts/validate.py" "$@"
