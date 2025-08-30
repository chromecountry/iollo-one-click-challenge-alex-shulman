#!/bin/bash
set -euo pipefail

# Analysis pipeline runner script
# Ensures virtual environment is properly activated

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV_DIR="$SCRIPT_DIR/venv"

echo "📊 Running analysis pipeline..."

# Setup virtual environment if it doesn't exist
if [ ! -d "$VENV_DIR" ]; then
    echo "Setting up virtual environment..."
    python3 -m venv "$VENV_DIR"
    "$VENV_DIR/bin/pip" install -r "$SCRIPT_DIR/requirements.txt"
fi

# Run the coordinator with proper environment
echo "Starting data analysis pipeline..."
"$VENV_DIR/bin/python" "$SCRIPT_DIR/coordinator.py"