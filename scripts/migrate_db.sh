#!/bin/bash
if [ -d ".venv" ]; then
    source .venv/bin/activate
fi

echo "🗄️ Aplicando migraciones de base de datos..."
python -c "from core.migrations import run_migrations; print(run_migrations())"
