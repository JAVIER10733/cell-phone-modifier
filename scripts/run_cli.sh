#!/bin/bash
if [ -d ".venv" ]; then
    source .venv/bin/activate
fi

echo "🖥️ Iniciando CLI de CPM..."
python main.py --cli
