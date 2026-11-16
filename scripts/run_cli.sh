#!/bin/bash

# run_cli.sh - Inicia cell_phone_modifier en modo CLI
# Uso: ./run_cli.sh [--dry-run] [--debug]

set -e

PROJECT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
cd "$PROJECT_DIR"

echo "╔═══════════════════════════════════════════════════════════════╗"
echo "║              cell_phone_modifier - Modo CLI                   ║"
echo "╚═══════════════════════════════════════════════════════════════╝"
echo ""

# Parsear argumentos
DRY_RUN=""
DEBUG=""

while [[ $# -gt 0 ]]; do
    case $1 in
        --dry-run)
            DRY_RUN="--dry-run"
            echo "ℹ️  Modo dry-run activado"
            shift
            ;;
        --debug)
            DEBUG="--debug"
            echo "ℹ️  Modo debug activado"
            shift
            ;;
        --help)
            echo "Uso: ./run_cli.sh [--dry-run] [--debug]"
            echo ""
            echo "Opciones:"
            echo "  --dry-run   Simula acciones sin ejecutarlas"
            echo "  --debug     Activa logging detallado"
            echo "  --help      Muestra esta ayuda"
            exit 0
            ;;
        *)
            echo "⚠️  Opción desconocida: $1"
            exit 1
            ;;
    esac
done

# Verificar Python
if ! command -v python &> /dev/null; then
    echo "❌ Python no encontrado. Instala con: pkg install python"
    exit 1
fi

# Verificar dependencias mínimas
if ! python -c "import rich" &> /dev/null; then
    echo "⚠️  Rich no instalado. Instalando..."
    pip install rich
fi

# Verificar entorno
if [ "$PREFIX" != "/data/data/com.termux/files/usr" ]; then
    echo "⚠️  No estás en Termux. Algunas funciones pueden no funcionar."
    echo "   Presiona Ctrl+C para cancelar, o Enter para continuar..."
    read -r
fi

# Ejecutar
echo "🚀 Iniciando cell_phone_modifier..."
echo ""

python main.py $DRY_RUN $DEBUG

# Código de salida
EXIT_CODE=$?

if [ $EXIT_CODE -eq 0 ]; then
    echo ""
    echo "✅ Aplicación cerrada correctamente"
else
    echo ""
    echo "❌ Aplicación cerrada con errores (código: $EXIT_CODE)"
    echo "   Revisa logs/app.log para más detalles"
fi

exit $EXIT_CODE