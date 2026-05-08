#!/bin/bash

# Define the absolute path to the hypercorn binary inside the venv
HYPERCORN_BIN="$(pwd)/venv/bin/hypercorn"

# Check if the binary exists and is executable
if [ ! -x "$HYPERCORN_BIN" ]; then
    echo "Error: Hypercorn not found or not executable at $HYPERCORN_BIN"
    echo "Trying to fix permissions..."
    chmod +x "$HYPERCORN_BIN"
fi

WITH_SSL="N"
while [[ "$#" -gt 0 ]]; do
    case $1 in
        --withssl) WITH_SSL="$2"; shift ;;
        *) echo "Unknown parameter passed: $1"; exit 1 ;;
    esac
    shift
done

# Base command
CMD="$HYPERCORN_BIN main:app --bind 0.0.0.0:6798"

if [[ "$WITH_SSL" =~ ^[Yy]$ ]]; then
    echo "--- Starting Hypercorn with SSL (using venv) ---"
    CMD="$CMD --certfile ./ssl/rareHashes.crt --keyfile ./ssl/rareHashes.key"
else
    echo "--- Starting Hypercorn in HTTP mode (using venv) ---"
fi

echo "--- Starting Hypercorn (using venv) ---"
exec $CMD