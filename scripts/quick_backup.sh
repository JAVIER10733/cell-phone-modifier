#!/bin/bash
if [ -d ".venv" ]; then
    source .venv/bin/activate
fi

echo "💾 Iniciando respaldo de CPM..."
python main.py backup create
