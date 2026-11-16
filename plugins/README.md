# 🧩 Sistema de Plugins

## ¿Qué es un plugin?

Un plugin es un módulo personalizado que extiende las funcionalidades de `cell_phone_modifier` sin modificar el código base.

## Estructura de un plugin

plugins/
└── mi_plugin/
├── init.py # Metadata del plugin
└── plugin.py # Código del plugin

## Cómo crear un plugin

### 1. Crear la estructura

````bash
mkdir -p plugins/mi_plugin
touch plugins/mi_plugin/__init__.py
touch plugins/mi_plugin/plugin.py

2. Escribir el plugin
from core.modules.base import BaseModule

class MiPlugin(BaseModule):
    name = "mi_plugin"
    description = "Descripción de mi plugin"
    requires_device = True
    requires_root = False
    danger_level = "low"

    def execute(self, **kwargs):
        # Tu lógica aquí
        return {"resultado": "ok"}

        3. Registrar el plugin
Opción A: Auto-registro en __init__.py:
from plugins.mi_plugin.plugin import MiPlugin
from core.modules.registry import registry
registry.register(MiPlugin)

Opción B: Cargar dinámicamente desde la CLI:

python -c "from core.plugin_runner import PluginRunner; PluginRunner().load_plugin('mi_plugin')"

Ejemplo completo
Ver example_plugin/ para un plugin funcional de referencia.
Reglas
Herencia: Tu plugin debe heredar de BaseModule
Nombre único: El atributo name debe ser único
Sin dependencias externas pesadas: Usa solo lo que está en requirements.txt
Manejo de errores: Captura excepciones y usa logger
Documentación: Incluye docstrings en todas las funciones públicas
Plugins de la comunidad
¿Creaste un plugin útil? ¡Compártelo!
Abre un issue con la etiqueta plugin
O haz un pull request a la carpeta plugins/community/



---

## 🔹 2. Carpeta `scripts/`

### Archivo: `cell_phone_modifier/scripts/check_env.sh`

```bash
#!/bin/bash

# check_env.sh - Verifica el entorno de Termux para cell_phone_modifier
# Compatible con Termux en Android

set -e

echo "╔═══════════════════════════════════════════════════════════════╗"
echo "║          Verificación de Entorno - cell_phone_modifier        ║"
echo "╚═══════════════════════════════════════════════════════════════╝"
echo ""

# Verificar Termux
if [ "$PREFIX" != "/data/data/com.termux/files/usr" ]; then
    echo "❌ Error: Este script solo funciona en Termux."
    echo "   Descarga Termux desde: https://f-droid.org/packages/com.termux/"
    exit 1
fi
echo "✅ Entorno Termux detectado"

# Verificar Python
if command -v python &> /dev/null; then
    PYTHON_VERSION=$(python --version 2>&1)
    echo "✅ Python: $PYTHON_VERSION"
else
    echo "❌ Python no encontrado. Instala con: pkg install python"
    exit 1
fi

# Verificar ADB
if command -v adb &> /dev/null; then
    ADB_VERSION=$(adb version 2>&1 | head -n 1)
    echo "✅ ADB: $ADB_VERSION"
else
    echo "❌ ADB no encontrado. Instala con: pkg install android-tools"
fi

# Verificar Fastboot
if command -v fastboot &> /dev/null; then
    FB_VERSION=$(fastboot --version 2>&1 | head -n 1)
    echo "✅ Fastboot: $FB_VERSION"
else
    echo "❌ Fastboot no encontrado. Instala con: pkg install android-tools"
fi

# Verificar Git
if command -v git &> /dev/null; then
    GIT_VERSION=$(git --version 2>&1)
    echo "✅ Git: $GIT_VERSION"
else
    echo "⚠️  Git no encontrado. Instala con: pkg install git"
fi

# Verificar termux-api
if command -v termux-notification &> /dev/null; then
    echo "✅ termux-api: Instalado"
else
    echo "⚠️  termux-api no instalado (opcional). Instala con: pkg install termux-api"
fi

# Verificar dependencias Python
echo ""
echo "=== Dependencias Python ==="

check_python_pkg() {
    if python -c "import $1" &> /dev/null; then
        echo "  ✅ $1"
    else
        echo "  ❌ $1 (instala con: pip install $1)"
    fi
}

check_python_pkg "dotenv"
check_python_pkg "yaml"
check_python_pkg "rich"
check_python_pkg "bottle"

# Verificar arquitectura
echo ""
echo "=== Arquitectura ==="
ARCH=$(uname -m)
echo "  Arquitectura: $ARCH"

if [ "$ARCH" = "aarch64" ] || [ "$ARCH" = "armv7l" ]; then
    echo "  ✅ Arquitectura compatible"
else
    echo "  ⚠️  Arquitectura no verificada: $ARCH"
fi

# Verificar almacenamiento
echo ""
echo "=== Almacenamiento ==="
if [ -d "$HOME/storage" ]; then
    echo "  ✅ Almacenamiento compartido accesible"
else
    echo "  ⚠️  Almacenamiento no configurado. Ejecuta: termux-setup-storage"
fi

# Verificar espacio libre
FREE_SPACE=$(df -h "$HOME" | tail -n 1 | awk '{print $4}')
echo "  Espacio libre: $FREE_SPACE"

# Verificar dispositivos ADB
echo ""
echo "=== Dispositivos ADB ==="
if command -v adb &> /dev/null; then
    DEVICES=$(adb devices 2>/dev/null | grep -c "device$" || echo "0")
    if [ "$DEVICES" -gt 0 ]; then
        echo "  ✅ $DEVICES dispositivo(s) conectado(s)"
        adb devices | grep "device$" | while read -r line; do
            echo "    - $line"
        done
    else
        echo "  ⚠️  No hay dispositivos conectados"
        echo "     Conecta un dispositivo por USB o usa ADB inalámbrico"
    fi
fi

# Resumen
echo ""
echo "╔═══════════════════════════════════════════════════════════════╗"
echo "║                    Verificación Completada                    ║"
echo "╚═══════════════════════════════════════════════════════════════╝"
echo ""
echo "Para instalar dependencias faltantes:"
echo "  pkg install android-tools git termux-api"
echo "  pip install -r requirements.txt"
echo ""
echo "Para ejecutar la aplicación:"
echo "  python main.py"


````
