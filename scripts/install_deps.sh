#!/bin/bash
echo "🚀 Instalando dependencias de CPM..."

# Detectar Termux
if [ -n "$PREFIX" ] && [[ "$PREFIX" == *"com.termux"* ]]; then
    echo "📱 Entorno Termux detectado."
    pkg update -y
    pkg install -y python android-tools termux-api
fi

# Crear entorno virtual si no existe
if [ ! -d ".venv" ]; then
    echo "🐍 Creando entorno virtual..."
    python -m venv .venv
fi

# Activar entorno e instalar dependencias de Python
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

echo "✅ ¡Dependencias instaladas con éxito!"
