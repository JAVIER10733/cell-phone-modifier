#!/bin/bash

# quick_backup.sh - Backup rápido de APKs con cell_phone_modifier
# Uso: ./quick_backup.sh [paquete] [directorio_destino]

set -e

PROJECT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
BACKUP_DIR="${2:-$PROJECT_DIR/data/backups}"

echo "╔═══════════════════════════════════════════════════════════════╗"
echo "║              Backup Rápido - cell_phone_modifier              ║"
echo "╚═══════════════════════════════════════════════════════════════╝"
echo ""

# Verificar que existe el proyecto
if [ ! -f "$PROJECT_DIR/main.py" ]; then
    echo "❌ Error: No se encontró cell_phone_modifier en $PROJECT_DIR"
    exit 1
fi

# Verificar ADB
if ! command -v adb &> /dev/null; then
    echo "❌ ADB no encontrado. Instala con: pkg install android-tools"
    exit 1
fi

# Verificar dispositivos
DEVICES=$(adb devices | grep -c "device$" || echo "0")
if [ "$DEVICES" -eq 0 ]; then
    echo "❌ No hay dispositivos conectados"
    echo "   Conecta un dispositivo por USB o usa ADB inalámbrico"
    exit 1
fi

# Crear directorio de backup
mkdir -p "$BACKUP_DIR"
mkdir -p "$BACKUP_DIR/apks"

TIMESTAMP=$(date +%Y%m%d_%H%M%S)
BACKUP_PATH="$BACKUP_DIR/backup_$TIMESTAMP"
mkdir -p "$BACKUP_PATH"

echo "📁 Directorio de backup: $BACKUP_PATH"
echo ""

if [ -n "$1" ]; then
    # Backup de un paquete específico
    PACKAGE="$1"
    echo "📦 Haciendo backup de: $PACKAGE"
    
    python "$PROJECT_DIR/main.py" --backup-apk "$PACKAGE" --output "$BACKUP_PATH" 2>/dev/null || \
    python -c "
import sys
sys.path.insert(0, '$PROJECT_DIR')
from core.modules.backup import BackupModule
from core.adb_wrapper import ADBWrapper

adb = ADBWrapper()
module = BackupModule(adb)
path = module.backup_apk('$PACKAGE', '$BACKUP_PATH')
print(f'✅ APK guardado en: {path}')
"
else
    # Backup de todos los APKs
    echo "📦 Haciendo backup de TODAS las aplicaciones..."
    echo "   Esto puede tardar varios minutos..."
    echo ""
    
    python -c "
import sys
sys.path.insert(0, '$PROJECT_DIR')
from core.modules.backup import BackupModule
from core.adb_wrapper import ADBWrapper

adb = ADBWrapper()
module = BackupModule(adb)
paths = module.backup_all_apks('$BACKUP_PATH')
print(f'\\n✅ {len(paths)} APKs guardados en: $BACKUP_PATH')
"
fi

# Crear manifest
echo ""
echo "📝 Creando manifest..."
cat > "$BACKUP_PATH/manifest.json" << EOF
{
  "timestamp": "$TIMESTAMP",
  "backup_dir": "$BACKUP_PATH",
  "device": "$(adb shell getprop ro.product.model 2>/dev/null || echo 'unknown')",
  "android_version": "$(adb shell getprop ro.build.version.release 2>/dev/null || echo 'unknown')",
  "tool": "cell_phone_modifier",
  "tool_version": "0.1.0"
}
EOF

echo ""
echo "╔═══════════════════════════════════════════════════════════════╗"
echo "║                     Backup Completado                         ║"
echo "╚═══════════════════════════════════════════════════════════════╝"
echo ""
echo "📁 Ubicación: $BACKUP_PATH"
echo "📊 Manifest: $BACKUP_PATH/manifest.json"
echo ""
echo "Para restaurar:"
echo "  python main.py  →  Backup y Restauración  →  Restaurar APK"