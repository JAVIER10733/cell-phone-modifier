# 📱 cell_phone_modifier

Herramienta de modificación de dispositivos Android desde **Termux**.

![Version](https://img.shields.io/badge/version-0.1.0-blue)
![Python](https://img.shields.io/badge/python-3.8+-green)
![Platform](https://img.shields.io/badge/platform-Termux-orange)
![License](https://img.shields.io/badge/license-MIT-yellow)

## ✨ Características

- ✅ **100% compatible con Termux** (Android aarch64/armv7)
- ✅ **Sin root requerido** para funciones básicas
- ✅ **Detección automática de root** y Magisk
- ✅ **ADB inalámbrico** (pairing Android 11+)
- ✅ **20+ módulos funcionales** (info, apps, archivos, backup, logs, etc.)
- ✅ **CLI interactiva** con Rich (colores, tablas, menús)
- ✅ **Dashboard web local** con Bottle
- ✅ **Perfiles por fabricante** (Samsung, Pixel, Xiaomi)
- ✅ **Sistema de plugins** extensible
- ✅ **Base de datos SQLite** para historial
- ✅ **Tests automatizados** con pytest
- ✅ **Documentación completa** en español

## 🚀 Instalación rápida

````bash
# 1. Clonar el repositorio
git clone https://github.com/JAVIER10733/cell-phone-modifier.git
cd cell-phone-modifier

# 2. Instalar dependencias
chmod +x setup.sh
./setup.sh

# 3. Ejecutar
python main.py

Uso
Menú interactivo

python main.py

Accederás a un menú con 12 opciones:
📱 Dispositivo - Info, batería, almacenamiento, reinicio
🔌 Conexión - USB, WiFi pairing, WiFi directo
💾 Backup y Restauración - APKs, backup completo
📦 Aplicaciones - Listar, instalar, desinstalar
📁 Archivos - Listar, pull, push, eliminar
🔍 Diagnóstico - Capturas, logcat
🔒 Seguridad - (En desarrollo)
⚙️ Tweaks - (En desarrollo)
🤖 Automatización - (En desarrollo)
⚙️ Configuración - Ver/editar config
📊 Estado del Sistema - Info y dependencias
🌐 Dashboard Web - Servidor web local
🚪 Salir
Comandos directos

# Ver dispositivos conectados
python -c "from core.adb_wrapper import ADBWrapper; print(ADBWrapper().get_devices())"

# Información del dispositivo
python -c "from core.modules.device_info import DeviceInfoModule; DeviceInfoModule().print_info()"

# Lista de apps
python -c "from core.modules.apps import AppsModule; print(AppsModule().list_packages())"

# Captura de pantalla
python -c "from core.modules.screenshots import ScreenshotsModule; print(ScreenshotsModule().take_screenshot())"

# Dashboard web
python -c "from web.server import create_server; create_server().start()"

📁 Estructura del proyecto
cell_phone_modifier/
├── main.py                 # Punto de entrada
├── setup.sh                # Instalador
├── requirements.txt        # Dependencias Python
├── requirements_dev.txt    # Dependencias de desarrollo
├── core/                   # Núcleo del proyecto
│   ├── adb_wrapper.py      # Wrapper de ADB
│   ├── fastboot_wrapper.py # Wrapper de Fastboot
│   ├── config.py           # Configuración
│   ├── logger.py           # Sistema de logs
│   ├── modules/            # 20+ módulos funcionales
│   └── drivers/            # Drivers por fabricante
├── cli/                    # Interfaz CLI con Rich
├── web/                    # Dashboard web (Bottle)
├── config/                 # Configuración y perfiles
├── tests/                  # Tests con pytest
├── docs/                   # Documentación
├── scripts/                # Scripts de utilidad
├── plugins/                # Sistema de plugins
└── data/                   # Datos generados (backups, exports)

Tests

# Instalar dependencias de desarrollo
pip install -r requirements_dev.txt

# Ejecutar todos los tests
pytest

# Con cobertura
pytest --cov=core --cov-report=term-missing

# Solo unitarios
pytest tests/unit/

# Solo integración
pytest tests/integration/

Módulos disponibles

Módulo
Descripción
Root
device_info
Info completa del dispositivo
❌
battery
Estado de batería
❌
storage
Particiones y uso
❌
apps
Gestión de aplicaciones
❌
files
Gestión de archivos
❌
screenshots
Capturas y grabación
❌
backup
Backup de APKs
❌
restore
Restauración
❌
logs
Logcat y dmesg
❌
network
Red WiFi/celular
❌
processes
Procesos en ejecución
❌
input_control
Tap, swipe, texto
❌
root
Detección de root
❌
developer
Opciones de desarrollador
❌
diagnostics
Diagnósticos del sistema
❌
privacy
Permisos de apps
❌
automation
Macros y secuencias
❌
profiles
Perfiles por fabricante
❌
notifications
Notificaciones termux-api
⚠️
scheduler
Tareas programadas
⚠️


📱 Conexión ADB Inalámbrica
Android 11+ (Pairing)
En el dispositivo: Opciones de desarrollador → Depuración inalámbrica → Emparejar
Anota el código de 6 dígitos y la IP:puerto
En Termux:


adb pair <IP>:<puerto>
# Ingresa el código
adb connect <IP>:<puerto_de_depuracion>

Android 10 o inferior
Conecta por USB y activa depuración USB
Ejecuta:

adb tcpip 5555
adb connect <IP>:5555
# Desconecta el USB

⚠️ Limitaciones
Sin root: Algunas funciones están limitadas
adb backup obsoleto: Android 12+ limita backups
Contactos/SMS/Call logs: Requieren permisos especiales
Fastboot: Solo información, no flasheo (riesgo de brick)
Web dashboard: Solo HTTP, sin autenticación robusta
dmesg: Puede requerir root en algunos dispositivos
🛡️ Seguridad
Todas las acciones destructivas requieren confirmación
Modo dry-run disponible para simular acciones
Confirmación doble para acciones críticas (flash, wipe)
Perfiles con listas de paquetes protegidos por fabricante
Nunca expongas el dashboard web en redes públicas
🤝 Contribuir
Fork el repositorio
Crea una rama (git checkout -b feature/nueva)
Commit (git commit -m 'Añadir feature')
Push (git push origin feature/nueva)
Abre un Pull Request
📄 Licencia
MIT - Ver LICENSE
👤 Autor
Ythan Javier Mora Gamarra
📧 ythanjavier6@gmail.com
📱 +593 991459589
💼 LinkedIn
💻 GitHub
📍 Ventanas, Los Ríos, Ecuador
📚 Documentación
Guía de instalación en Termux
Módulos disponibles
Guía de la CLI
Guía de seguridad
Solución de problemas



---

## Archivo: `cell_phone_modifier/requirements.txt`

```txt
# Dependencias principales de cell_phone_modifier
# Instalar con: pip install -r requirements.txt

python-dotenv>=1.0.0
pyyaml>=6.0
rich>=13.0.0
bottle>=0.12.25

````
