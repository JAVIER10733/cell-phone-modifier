#!/bin/bash
PROJECT_DIR=$(pwd)
LOG_DIR="$PROJECT_DIR/logs"
mkdir -p "$LOG_DIR"

echo "🤖 Iniciando daemon de CPM en segundo plano..."
nohup python main.py web > "$LOG_DIR/daemon.log" 2>&1 &

# Adquirir WakeLock si estamos en Termux
if command -v termux-wake-lock &> /dev/null; then
    termux-wake-lock
fi

echo "✅ Daemon iniciado. Revisa $LOG_DIR/daemon.log para más detalles."
