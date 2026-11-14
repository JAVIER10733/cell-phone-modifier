#!/bin/bash
echo "🔍 Verificando entorno de CPM..."

# Verificar Python
if command -v python &> /dev/null; then
    echo "✅ Python instalado: $(python --version)"
else
    echo "❌ Python no encontrado. Instálalo primero."
    exit 1
fi

# Verificar ADB
if command -v adb &> /dev/null || command -v termux-adb &> /dev/null; then
    echo "✅ ADB detectado."
else
    echo "⚠️ ADB no encontrado. Las funciones de dispositivo externo no funcionarán."
fi

# Verificar entorno virtual
if [ -d ".venv" ]; then
    echo "✅ Entorno virtual encontrado."
else
    echo "⚠️ Entorno virtual no encontrado. Ejecuta './scripts/install_deps.sh'."
fi
