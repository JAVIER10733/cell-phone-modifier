# 📱 cell_phone_modifier

Herramienta para modificar y gestionar dispositivos Android desde Termux.

![Version](https://img.shields.io/badge/version-0.1.0-blue)
![Python](https://img.shields.io/badge/python-3.8+-green)
![Platform](https://img.shields.io/badge/platform-Termux-orange)
![License](https://img.shields.io/badge/license-MIT-yellow)

## ✨ Características

+ ✅ 100% compatible con Termux (Android aarch64 y armv7)
+ ✅ Sin root para las funciones básicas
+ ✅ Detección automática de root y Magisk
+ ✅ ADB inalámbrico (pairing en Android 11+)
+ ✅ 20 módulos funcionales: info, apps, archivos, backup, logs y más
+ ✅ CLI interactiva con Rich: colores, tablas y menús
+ ✅ Dashboard web local con Bottle
+ ✅ Perfiles por fabricante: Samsung, Pixel y Xiaomi
+ ✅ Sistema de plugins extensible
+ ✅ Base de datos SQLite para el historial
+ ✅ Tests automatizados con pytest
+ ✅ Documentación completa en español

## 🚀 Instalación rápida

```bash
# 1. Clona el repositorio
git clone https://github.com/JAVIER10733/cell-phone-modifier.git
cd cell-phone-modifier

# 2. Instala las dependencias
chmod +x setup.sh
./setup.sh

# 3. Ejecuta
python main.py
```

## 🕹️ Uso

### Menú interactivo

```bash
python main.py
```

Verás un menú con 13 opciones:

| Opción | Descripción | Estado |
|---|---|---|
| 📱 Dispositivo | Info, batería, almacenamiento, reinicio | Listo |
| 🔌 Conexión | USB, WiFi pairing, WiFi directo | Listo |
| 💾 Backup y Restauración | APKs y backup completo | Listo |
| 📦 Aplicaciones | Listar, instalar, desinstalar | Listo |
| 📁 Archivos | Listar, pull, push, eliminar | Listo |
| 🔍 Diagnóstico | Capturas y logcat | Listo |
| 🔒 Seguridad | Próximamente | En desarrollo |
| ⚙️ Tweaks | Próximamente | En desarrollo |
| 🤖 Automatización | Próximamente | En desarrollo |
| ⚙️ Configuración | Ver y editar config | Listo |
| 📊 Estado del Sistema | Info y dependencias | Listo |
| 🌐 Dashboard Web | Servidor web local | Listo |
| 🚪 Salir | Cierra la herramienta | Listo |

### Comandos directos

```bash
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
```

## 📁 Estructura del proyecto

```text
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
│   ├── modules/            # 20 módulos funcionales
│   └── drivers/            # Drivers por fabricante
├── cli/                    # Interfaz CLI con Rich
├── web/                    # Dashboard web (Bottle)
├── config/                 # Configuración y perfiles
├── tests/                  # Tests con pytest
├── docs/                   # Documentación
├── scripts/                # Scripts de utilidad
├── plugins/                # Sistema de plugins
└── data/                   # Datos generados (backups, exports)
```

## 🧪 Tests

```bash
# Instala las dependencias de desarrollo
pip install -r requirements_dev.txt

# Ejecuta todos los tests
pytest

# Con cobertura
pytest --cov=core --cov-report=term-missing

# Unitarios
pytest tests/unit/

# Integración
pytest tests/integration/
```

## 🧩 Módulos disponibles

| Módulo | Descripción | Requiere |
|---|---|---|
| device_info | Info completa del dispositivo | Nada extra |
| battery | Estado de batería | Nada extra |
| storage | Particiones y uso | Nada extra |
| apps | Gestión de aplicaciones | Nada extra |
| files | Gestión de archivos | Nada extra |
| screenshots | Capturas y grabación | Nada extra |
| backup | Backup de APKs | Nada extra |
| restore | Restauración | Nada extra |
| logs | Logcat y dmesg | Nada extra |
| network | Red WiFi y celular | Nada extra |
| processes | Procesos en ejecución | Nada extra |
| input_control | Tap, swipe y texto | Nada extra |
| root | Detección de root | Nada extra |
| developer | Opciones de desarrollador | Nada extra |
| diagnostics | Diagnósticos del sistema | Nada extra |
| privacy | Permisos de apps | Nada extra |
| automation | Macros y secuencias | Nada extra |
| profiles | Perfiles por fabricante | Nada extra |
| notifications | Notificaciones | termux-api |
| scheduler | Tareas programadas | termux-api |

## 📱 Conexión ADB inalámbrica

### Android 11 o superior (pairing)

1. En el dispositivo ve a Opciones de desarrollador, Depuración inalámbrica y toca Emparejar.
2. Anota el código de 6 dígitos y la IP:puerto.
3. En Termux ejecuta:

```bash
adb pair <IP>:<puerto>
# Ingresa el código
adb connect <IP>:<puerto_de_depuracion>
```

### Android 10 o inferior

1. Conecta por USB y activa la depuración USB.
2. Ejecuta:

```bash
adb tcpip 5555
adb connect <IP>:5555
# Desconecta el USB
```

## ⚠️ Limitaciones

+ Sin root, algunas funciones tienen límites.
+ `adb backup` está obsoleto. Android 12+ limita los backups.
+ Contactos, SMS y registros de llamadas requieren permisos especiales.
+ Fastboot ofrece únicamente información. No flashea, para evitar el riesgo de brick.
+ El dashboard web usa HTTP y no tiene autenticación robusta.
+ `dmesg` requiere root en algunos dispositivos.

## 🛡️ Seguridad

+ Toda acción destructiva pide confirmación.
+ El modo dry-run simula las acciones sin ejecutarlas.
+ Las acciones críticas (flash, wipe) piden doble confirmación.
+ Cada perfil de fabricante incluye una lista de paquetes protegidos.
+ Nunca expongas el dashboard web en redes públicas.

## 🤝 Contribuir

1. Haz fork del repositorio.
2. Crea una rama: `git checkout -b feature/nueva`
3. Haz commit: `git commit -m 'Añadir feature'`
4. Sube la rama: `git push origin feature/nueva`
5. Abre un Pull Request.

## 📚 Documentación

+ [Guía de instalación en Termux](docs/instalacion.md)
+ [Módulos disponibles](docs/modulos.md)
+ [Guía de la CLI](docs/cli.md)
+ [Guía de seguridad](docs/seguridad.md)
+ [Solución de problemas](docs/troubleshooting.md)

## 📄 Licencia

MIT. Mira el archivo [LICENSE](LICENSE).

## 👤 Autor

Ythan Javier Mora Gamarra

📧 ythanjavier6@gmail.com
📱 +593 991459589
💼 LinkedIn
💻 GitHub
📍 Ventanas, Los Ríos, Ecuador
