#!/bin/bash

# setup.sh - Instalación de cell_phone_modifier en Termux
# Autor: Ythan Javier Mora Gamarra
# Versión: 0.1.0

set -e

echo "╔═══════════════════════════════════════════════════════════════╗"
echo "║                                                               ║"
echo "║          cell_phone_modifier - Instalación en Termux         ║"
echo "║                                                               ║"
echo "╚═══════════════════════════════════════════════════════════════╝"
echo ""

# Verificar que estamos en Termux
if [ "$PREFIX" != "/data/data/com.termux/files/usr" ]; then
    echo "❌ Error: Este script solo funciona en Termux."
    echo "   Descarga Termux desde: https://f-droid.org/packages/com.termux/"
    exit 1
fi

echo "✅ Entorno Termux detectado"
echo ""

# Actualizar paquetes
echo "📦 Actualizando paquetes..."
pkg update -y
pkg upgrade -y
echo ""

# Instalar dependencias del sistema
echo "📦 Instalando dependencias del sistema..."
pkg install -y python android-tools git
echo ""

# Instalar dependencias de Python
echo "📦 Instalando dependencias de Python..."
pip install --upgrade pip
pip install -r requirements.txt
echo ""

# Instalar dependencias de desarrollo (opcional)
read -p "¿Instalar dependencias de desarrollo? (pytest, ruff, mypy) [y/N]: " install_dev
if [[ "$install_dev" =~ ^[Yy]$ ]]; then
    echo "📦 Instalando dependencias de desarrollo..."
    pip install -r requirements_dev.txt
    echo ""
fi

# Instalar termux-api (opcional)
read -p "¿Instalar termux-api? (notificaciones, batería, etc.) [y/N]: " install_api
if [[ "$install_api" =~ ^[Yy]$ ]]; then
    echo "📦 Instalando termux-api..."
    pkg install -y termux-api
    echo ""
fi

# Configurar almacenamiento (opcional)
read -p "¿Configurar acceso al almacenamiento compartido? [y/N]: " setup_storage
if [[ "$setup_storage" =~ ^[Yy]$ ]]; then
    echo "📱 Configurando almacenamiento..."
    termux-setup-storage
    echo ""
fi

# Crear directorios necesarios
echo "📁 Creando directorios..."
mkdir -p logs
mkdir -p data/backups
mkdir -p data/exports
mkdir -p config/profiles
echo ""

# Crear .env si no existe
if [ ! -f .env ]; then
    echo "⚙️  Creando archivo .env..."
    cp .env.example .env
    echo "✅ Archivo .env creado. Edítalo si necesitas cambiar la configuración."
    echo ""
fi

# Dar permisos de ejecución a scripts
echo "🔧 Configurando permisos..."
chmod +x main.py
chmod +x setup.sh
chmod +x scripts/*.sh 2>/dev/null || true
echo ""

# Verificar instalación
echo "🔍 Verificando instalación..."
python --version
adb version 2>/dev/null | head -n 1 || echo "⚠️  ADB no disponible"
fastboot --version 2>/dev/null | head -n 1 || echo "⚠️  Fastboot no disponible"
echo ""

# Ejecutar tests si están instalados
if python -c "import pytest" 2>/dev/null; then
    read -p "¿Ejecutar tests? [y/N]: " run_tests
    if [[ "$run_tests" =~ ^[Yy]$ ]]; then
        echo "🧪 Ejecutando tests..."
        pytest tests/unit/ -v
        echo ""
    fi
fi

echo "╔═══════════════════════════════════════════════════════════════╗"
echo "║                                                               ║"
echo "║                   ✅ Instalación Completada                  ║"
echo "║                                                               ║"
echo "╚═══════════════════════════════════════════════════════════════╝"
echo ""
echo "Para ejecutar la aplicación:"
echo "  python main.py"
echo ""
echo "Para verificar dependencias:"
echo "  python -c 'from core.dependencies import check_dependencies; check_dependencies()'"
echo ""
echo "Para ejecutar el dashboard web:"
echo "  python -c 'from web.server import create_server; create_server().start()'"
echo ""
echo "Documentación:"
echo "  cat docs/termux_setup.md"
echo ""