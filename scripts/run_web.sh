#!/bin/bash
if [ -d ".venv" ]; then
    source .venv/bin/activate
fi

echo "🌐 Iniciando Dashboard en http://127.0.0.1:8722..."
python main.py web
