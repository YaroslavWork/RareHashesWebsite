#!/bin/bash

set -euo pipefail

# ---------------------------------------------------------------------------
# Local development runner (Hypercorn)
#
# Usage:
#   ./run.sh                 # HTTP, bind address from HOST in .env
#   ./run.sh --withssl y     # HTTPS, certificates from ./ssl
#   ./run.sh --withssl       # same as --withssl y
#   ./run.sh --help
# ---------------------------------------------------------------------------

# Work from the directory this script lives in, so relative paths
# (main:app, .env, ./ssl) resolve no matter where the script is called from.
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

VENV_DIR="${VENV_DIR:-$SCRIPT_DIR/venv}"
HYPERCORN_BIN="$VENV_DIR/bin/hypercorn"

CERT_FILE="${CERT_FILE:-$SCRIPT_DIR/ssl/rareHashes.crt}"
KEY_FILE="${KEY_FILE:-$SCRIPT_DIR/ssl/rareHashes.key}"

DEFAULT_HOST="0.0.0.0:6798"

WITH_SSL="N"

usage() {
    echo "Usage: $0 [--withssl [y|n]] [--help]"
    echo "  --withssl [y|n]  Serve over HTTPS using $CERT_FILE and $KEY_FILE (default: n)"
    echo "  --help           Show this message"
}

while [[ "$#" -gt 0 ]]; do
    case "$1" in
        --withssl)
            # Accept both "--withssl" (means y) and "--withssl y|n".
            if [[ "$#" -ge 2 && "$2" != --* ]]; then
                WITH_SSL="$2"
                shift
            else
                WITH_SSL="Y"
            fi
            ;;
        -h|--help)
            usage
            exit 0
            ;;
        *)
            echo "Unknown parameter passed: $1" >&2
            usage >&2
            exit 1
            ;;
    esac
    shift
done

# --- Check the virtual environment ---
if [ ! -x "$HYPERCORN_BIN" ]; then
    echo "Hypercorn not found or not executable at $HYPERCORN_BIN" >&2
    echo "Trying to fix permissions..." >&2
    chmod +x "$HYPERCORN_BIN" 2>/dev/null || true
    if [ ! -x "$HYPERCORN_BIN" ]; then
        echo "Error: cannot run Hypercorn. Install the dependencies first:" >&2
        echo "    $VENV_DIR/bin/pip install -r requirements-dev.txt" >&2
        exit 1
    fi
fi

# --- Read the bind address from .env (the same value main.py uses) ---
if [ ! -f "$SCRIPT_DIR/.env" ]; then
    echo "Error: .env not found in $SCRIPT_DIR. Create it (see readme.md)." >&2
    exit 1
fi

# "|| true" keeps grep's exit status 1 (no match) from aborting under "set -e".
BIND="$(grep -E '^[[:space:]]*HOST[[:space:]]*=' "$SCRIPT_DIR/.env" | tail -n 1 | cut -d '=' -f 2- | tr -d "\"' \r")" || true
BIND="${BIND#*://}"

if [ -z "$BIND" ]; then
    echo "Warning: HOST is not set in .env, falling back to $DEFAULT_HOST." >&2
    BIND="$DEFAULT_HOST"
fi

# --- Build the command ---
CMD=("$HYPERCORN_BIN" main:app --bind "$BIND")

if [[ "$WITH_SSL" =~ ^[Yy]$ ]]; then
    if [ ! -f "$CERT_FILE" ] || [ ! -f "$KEY_FILE" ]; then
        echo "Error: SSL certificate or key not found ($CERT_FILE, $KEY_FILE)." >&2
        echo "Create them in ./ssl (see readme.md) or run without --withssl." >&2
        exit 1
    fi
    echo "--- Starting Hypercorn with SSL (using venv) on $BIND ---"
    CMD+=(--certfile "$CERT_FILE" --keyfile "$KEY_FILE")
else
    echo "--- Starting Hypercorn in HTTP mode (using venv) on $BIND ---"
fi

exec "${CMD[@]}"
