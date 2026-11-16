<div align="center">

![Header](https://capsule-render.vercel.app/api?type=venom&color=0:0f2027,50:19c3a6,100:2c5364&height=280&section=header&text=cell_phone_modifier&fontSize=60&fontColor=ffffff&animation=twinkling&fontAlignY=38&desc=Controla%20tu%20Android%20desde%20Termux%20como%20un%20pro%20%F0%9F%9A%80&descAlignY=62&descSize=22)

[![Typing SVG](https://readme-typing-svg.demolab.com?font=Fira+Code&weight=600&size=22&pause=1000&color=19C3A6&center=true&vCenter=true&width=700&lines=Sin+root+para+lo+b%C3%A1sico+%F0%9F%93%B1%3BADB+inal%C3%A1mbrico+en+Android+11%2B+%F0%9F%93%A1%3B+20%2B+m%C3%B3dulos+listos+para+usar+%E2%9A%A1%3BDashboard+web+local+%F0%9F%8C%90%3B100%25+C%C3%B3digo+Abierto+%F0%9F%92%9A)](https://git.io/typing-svg)

<!-- Badges Principales -->
[![Version](https://img.shields.io/badge/version-0.1.0-blue?style=for-the-badge&logo=git&logoColor=white)](https://github.com/JAVIER10733/cell-phone-modifier/releases)
[![Python](https://img.shields.io/badge/python-3.8+-green?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Platform](https://img.shields.io/badge/platform-Termux-orange?style=for-the-badge&logo=android&logoColor=white)](https://termux.dev/)
[![License](https://img.shields.io/badge/license-MIT-yellow?style=for-the-badge&logo=opensourceinitiative&logoColor=white)](LICENSE)

<!-- Badges Secundarios -->
[![GitHub Stars](https://img.shields.io/github/stars/JAVIER10733/cell-phone-modifier?style=social)](https://github.com/JAVIER10733/cell-phone-modifier/stargazers)
[![GitHub Forks](https://img.shields.io/github/forks/JAVIER10733/cell-phone-modifier?style=social)](https://github.com/JAVIER10733/cell-phone-modifier/network/members)
[![GitHub Issues](https://img.shields.io/github/issues/JAVIER10733/cell-phone-modifier?style=social)](https://github.com/JAVIER10733/cell-phone-modifier/issues)
[![GitHub Pull Requests](https://img.shields.io/github/issues-pr/JAVIER10733/cell-phone-modifier?style=social)](https://github.com/JAVIER10733/cell-phone-modifier/pulls)

<br>

![Stack](https://skillicons.dev/icons?i=python,bash,sqlite,linux,android,git,html,css,js)

<br>

**🌐 [Ver Demo en Vivo](https://javier10733.github.io/cell-phone-modifier/index.html)** | **📚 [Documentación](docs/)** | **🐛 [Reportar Bug](https://github.com/JAVIER10733/cell-phone-modifier/issues)** | **💡 [Sugerir Mejora](https://github.com/JAVIER10733/cell-phone-modifier/issues)**

</div>

---

## 📖 Tabla de Contenidos

- [🎯 Visión General](#-visión-general)
- [✨ Características Principales](#-características-principales)
- [🚀 Instalación Rápida](#-instalación-rápida)
- [🕹️ Interfaz de la Herramienta](#️-interfaz-de-la-herramienta)
- [🧩 Módulos Disponibles](#-módulos-disponibles)
- [📱 Conexión ADB Inalámbrica](#-conexión-adb-inalámbrica)
- [🏗️ Arquitectura del Proyecto](#️-arquitectura-del-proyecto)
- [🧪 Tests y Calidad de Código](#-tests-y-calidad-de-código)
- [🗺️ Roadmap del Proyecto](#️-roadmap-del-proyecto)
- [⚠️ Limitaciones Conocidas](#️-limitaciones-conocidas)
- [🛡️ Seguridad](#️-seguridad)
- [🤝 Cómo Contribuir](#-cómo-contribuir)
- [📚 Documentación Adicional](#-documentación-adicional)
- [❓ Preguntas Frecuentes](#-preguntas-frecuentes)
- [📄 Licencia](#-licencia)
- [👤 Autor](#-autor)
- [🌟 Agradecimientos](#-agradecimientos)

---

## 🎯 Visión General

**cell_phone_modifier** nace de la necesidad de tener una herramienta centralizada, potente y fácil de usar para gestionar dispositivos Android directamente desde el entorno de **Termux**, sin depender de una PC. 

A diferencia de otras herramientas, este proyecto prioriza la **seguridad** (sin necesidad de root para lo esencial), la **extensibilidad** (arquitectura de plugins) y una experiencia de usuario **premium** dentro de la terminal (gracias a `Rich`).

> *"Tu dispositivo Android, bajo control total, desde la palma de tu mano."*

---

## ✨ Características Principales

<table>
<tr>
<td width="50%">

### 💪 Potencia y Compatibilidad
- ✅ **100% compatible** con Termux (aarch64 y armv7).
- ✅ **Sin root** para todas las funciones básicas.
- ✅ **Detección automática** de root y Magisk.
- ✅ **ADB Inalámbrico Nativo** (pairing Android 11+).
- ✅ **20+ módulos** funcionales listos para usar.
- ✅ **Perfiles por fabricante**: Samsung, Pixel y Xiaomi.

</td>
<td width="50%">

### 🎨 Experiencia y Extensibilidad
- ✅ **CLI interactiva** con `Rich`: colores, tablas y menús.
- ✅ **Dashboard web local** con Bottle.
- ✅ **Arquitectura de Plugins** extensible en Python.
- ✅ **Base de datos SQLite** para historial de acciones.
- ✅ **Tests automatizados** con `pytest`.
- ✅ **Documentación completa** en español.

</td>
</tr>
</table>

---

## 🚀 Instalación Rápida

Abre **Termux** (preferiblemente desde F-Droid) y ejecuta estos comandos:

```bash
# 1. Actualiza los paquetes base
pkg update && pkg upgrade -y

# 2. Clona el repositorio
git clone https://github.com/JAVIER10733/cell-phone-modifier.git
cd cell-phone-modifier

# 3. Ejecuta el instalador automático (instala dependencias de sistema y Python)
chmod +x setup.sh
./setup.sh

# 4. Inicia la herramienta
python main.py
```

> 💡 **Tip:** Si tienes problemas con `pip install`, recuerda que Termux maneja su propio entorno. Asegúrate de tener instalado `python-pip` vía `pkg install python-pip`.

---

## 🕹️ Interfaz de la Herramienta

Al ejecutar `python main.py`, se desplegará una interfaz de terminal (TUI) premium con el siguiente menú principal:

```text
╔══════════════════════════════════════════════════════════════════╗
║                                                                  ║
║   ██████╗███████╗██╗     ██╗     ██████╗ ██╗  ██╗ ██████╗        ║
║  ██╔════╝██╔════╝██║     ██║     ██╔══██╗██║  ██║██╔═══██╗       ║
║  ██║     █████╗  ██║     ██║     ██████╔╝███████║██║   ██║       ║
║  ██║     ██╔══╝  ██║     ██║     ██╔═══╝ ██╔══██║██║   ██║       ║
║  ╚██████╗███████╗███████╗███████╗██║     ██║  ██║╚██████╔╝       ║
║   ╚═════╝╚══════╝╚══════╝╚══════╝╚═╝     ╚═╝  ╚═╝ ╚═════╝        ║
║                                                                  ║
║                 PHONE MODIFIER - Termux Edition                  ║
║                            v0.1.0                                ║
╚══════════════════════════════════════════════════════════════════╝

=== Menú Principal ===
1. 📱 Dispositivo (Info, batería, reinicio)
2. 🔌 Conexión (USB, WiFi pairing)
3. 💾 Backup y Restauración
4. 📦 Aplicaciones
5. 📁 Archivos
6. 🔍 Diagnóstico (Capturas, Logs)
7. ⚙️ Configuración
8. 📊 Estado del Sistema
9. 🌐 Dashboard Web
0. 🚪 Salir
```

### Comandos Directos (Modo Script)

Si prefieres usar la herramienta de forma modular:

```bash
# Ver dispositivos conectados
python -c "from core.adb_wrapper import ADBWrapper; print(ADBWrapper().get_devices())"

# Información del dispositivo
python -c "from core.modules.device_info import DeviceInfoModule; DeviceInfoModule().print_info()"

# Lista de apps instaladas
python -c "from core.modules.apps import AppsModule; print(AppsModule().list_packages())"

# Tomar captura de pantalla
python -c "from core.modules.screenshots import ScreenshotsModule; print(ScreenshotsModule().take_screenshot())"

# Iniciar Dashboard Web
python -c "from web.server import create_server; create_server().start()"
```

---

## 🧩 Módulos Disponibles

<table>
<thead>
<tr>
<th align="left">Módulo</th>
<th align="left">Descripción</th>
<th align="left">Requiere</th>
<th align="left">Estado</th>
</tr>
</thead>
<tbody>
<tr><td><code>device_info</code></td><td>Información completa del dispositivo</td><td>Nada extra</td><td>🟢</td></tr>
<tr><td><code>battery</code></td><td>Estado y salud de la batería</td><td>Nada extra</td><td>🟢</td></tr>
<tr><td><code>storage</code></td><td>Particiones y uso de almacenamiento</td><td>Nada extra</td><td>🟢</td></tr>
<tr><td><code>apps</code></td><td>Gestión de aplicaciones instaladas</td><td>Nada extra</td><td>🟢</td></tr>
<tr><td><code>files</code></td><td>Gestión de archivos (pull/push)</td><td>Nada extra</td><td>🟢</td></tr>
<tr><td><code>screenshots</code></td><td>Capturas y grabación de pantalla</td><td>Nada extra</td><td>🟢</td></tr>
<tr><td><code>backup</code></td><td>Extracción de APKs y backups</td><td>Nada extra</td><td>🟢</td></tr>
<tr><td><code>restore</code></td><td>Restauración de backups</td><td>Nada extra</td><td>🟢</td></tr>
<tr><td><code>logs</code></td><td>Lectura de logcat y dmesg</td><td>Nada extra</td><td>🟢</td></tr>
<tr><td><code>network</code></td><td>Info de redes WiFi y celular</td><td>Nada extra</td><td>🟢</td></tr>
<tr><td><code>processes</code></td><td>Procesos en ejecución</td><td>Nada extra</td><td>🟢</td></tr>
<tr><td><code>input_control</code></td><td>Simulación de tap, swipe y texto</td><td>Nada extra</td><td>🟢</td></tr>
<tr><td><code>root</code></td><td>Detección de root y Magisk</td><td>Nada extra</td><td>🟢</td></tr>
<tr><td><code>developer</code></td><td>Opciones de desarrollador</td><td>Nada extra</td><td>🟢</td></tr>
<tr><td><code>diagnostics</code></td><td>Diagnósticos del sistema</td><td>Nada extra</td><td>🟢</td></tr>
<tr><td><code>privacy</code></td><td>Permisos de aplicaciones</td><td>Nada extra</td><td>🟢</td></tr>
<tr><td><code>automation</code></td><td>Macros y secuencias</td><td>Nada extra</td><td>🟡</td></tr>
<tr><td><code>profiles</code></td><td>Perfiles por fabricante</td><td>Nada extra</td><td>🟢</td></tr>
<tr><td><code>notifications</code></td><td>Gestión de notificaciones</td><td><code>termux-api</code></td><td>🟢</td></tr>
<tr><td><code>scheduler</code></td><td>Tareas programadas</td><td><code>termux-api</code></td><td>🟡</td></tr>
</tbody>
</table>

---

## 📱 Conexión ADB Inalámbrica

### Android 11 o superior (Pairing)

1. En el dispositivo ve a **Opciones de desarrollador > Depuración inalámbrica** y toca **Emparejar dispositivo con código**.
2. Anota el código de 6 dígitos y la dirección `IP:puerto`.
3. En Termux ejecuta:
```bash
adb pair <IP>:<puerto>
# Ingresa el código cuando se solicite
adb connect <IP>:<puerto_de_depuracion>
```

### Android 10 o inferior (Método clásico)

1. Conecta el dispositivo por USB y activa la **Depuración USB**.
2. Ejecuta los siguientes comandos:
```bash
adb tcpip 5555
adb connect <IP>:5555
# Ahora puedes desconectar el cable USB
```

---

## 🏗️ Arquitectura del Proyecto

```text
cell_phone_modifier/
│
├── 📄 main.py                 # Punto de entrada principal
├── ⚙️ setup.sh                # Script de instalación automática
├── 📦 requirements.txt        # Dependencias de Python
├── 📦 requirements_dev.txt    # Dependencias de desarrollo
│
├── 🧠 core/                   # Núcleo lógico del proyecto
│   ├── 🔌 adb_wrapper.py      # Wrapper para comandos ADB
│   ├── ⚡ fastboot_wrapper.py # Wrapper para comandos Fastboot
│   ├── ⚙️ config.py           # Gestión de configuración
│   ├── 📝 logger.py           # Sistema de logs
│   ├── 📂 modules/            # 20+ módulos funcionales
│   └── 🚗 drivers/            # Drivers específicos por fabricante
│
├── 💻 cli/                    # Interfaz de línea de comandos (Rich)
│   ├── 📋 menu.py             # Menú principal
│   ├── 🎨 colors.py           # Sistema de colores
│   ├── 🖥️ ui.py               # Componentes visuales
│   └── 📁 commands/           # Comandos específicos
│
├── 🌐 web/                    # Dashboard web (Bottle)
│   ├── 🖥️ server.py           # Servidor web local
│   └── 🎨 static/             # CSS, JS e imágenes
│
├── 🗄️ config/                 # Archivos de configuración y perfiles
├── 🧪 tests/                  # Suite de pruebas (pytest)
├── 📚 docs/                   # Documentación detallada
├── 🛠️ scripts/                # Scripts de utilidad
├── 🧩 plugins/                # Sistema de plugins de terceros
└── 💾 data/                   # Datos generados (backups, exports)
```

---

## 🧪 Tests y Calidad de Código

El proyecto mantiene altos estándares de calidad mediante pruebas automatizadas.

```bash
# Instala las dependencias de desarrollo
pip install -r requirements_dev.txt

# Ejecuta todos los tests
pytest

# Ejecuta tests con reporte de cobertura
pytest --cov=core --cov-report=term-missing

# Ejecuta solo tests unitarios
pytest tests/unit/

# Ejecuta solo tests de integración
pytest tests/integration/
```

---

## 🗺️ Roadmap del Proyecto

| Versión | Estado | Características Principales |
| :--- | :--- | :--- |
| **v0.1.0** | ✅ Actual | Lanzamiento inicial, 20+ módulos, ADB inalámbrico, perfiles base. |
| **v0.2.0** | 🚧 En desarrollo | Dashboard TUI interactivo, historial de comandos, temas personalizables. |
| **v0.3.0** | 📅 Planificado | Módulos de red y seguridad, auditoría de permisos, detección de apps maliciosas. |
| **v1.0.0** | 🔮 Futuro | Soporte multiplataforma (Linux, macOS, WSL), API pública para plugins de terceros, versión estable. |

---

## ⚠️ Limitaciones Conocidas

> [!WARNING]
> **Sin root**, algunas funciones avanzadas del sistema tienen límites.
> El comando `adb backup` está obsoleto y Android 12+ limita los backups de aplicaciones.
> Contactos, SMS y registros de llamadas requieren permisos especiales que no se pueden otorgar vía ADB sin root.
> **Fastboot** ofrece únicamente información. No realiza flasheos para evitar el riesgo de *brick*.
> El **dashboard web** usa HTTP y no tiene autenticación robusta; no lo expongas en redes públicas.
> El comando `dmesg` requiere root en algunos dispositivos.

---

## 🛡️ Seguridad

*   🔒 Toda acción destructiva **pide confirmación** previa.
*   🧪 El **modo dry-run** simula las acciones sin ejecutarlas.
*   ⚠️ Las acciones críticas (flash, wipe) piden **doble confirmación**.
*   📦 Cada perfil de fabricante incluye una **lista de paquetes protegidos**.
*   🚫 Nunca expongas el dashboard web en redes públicas.

---

## 🤝 Cómo Contribuir

¡Las contribuciones son bienvenidas! Si deseas mejorar el proyecto:

1. Haz un **fork** del repositorio.
2. Crea una rama para tu funcionalidad: `git checkout -b feature/nueva-funcionalidad`
3. Haz commit de tus cambios: `git commit -m 'Añadir nueva funcionalidad'`
4. Sube tu rama: `git push origin feature/nueva-funcionalidad`
5. Abre un **Pull Request**.

> Lee nuestra [Guía de Contribución](CONTRIBUTING.md) para más detalles.

---

## 📚 Documentación Adicional

| Documento | Descripción |
| :--- | :--- |
| [Guía de instalación](docs/instalacion.md) | Instalación paso a paso en Termux y solución de problemas. |
| [Módulos](docs/modulos.md) | Lista completa de módulos y ejemplos de uso. |
| [CLI](docs/cli.md) | Guía de la interfaz de línea de comandos. |
| [Seguridad](docs/seguridad.md) | Mejores prácticas y consideraciones de seguridad. |
| [Troubleshooting](docs/troubleshooting.md) | Solución de errores comunes. |

---

## ❓ Preguntas Frecuentes

<details>
<summary><b>¿Necesito root para usar la herramienta?</b></summary>
No. cell_phone_modifier está diseñado para funcionar exclusivamente con ADB, por lo que no requiere root ni modificaciones al sistema. Esto lo hace más seguro y compatible con la garantía de tu dispositivo.
</details>

<details>
<summary><b>¿Qué versiones de Android son compatibles?</b></summary>
Es compatible con Android 8.0 (Oreo) en adelante. El emparejamiento inalámbrico nativo requiere Android 11+, pero el método clásico de puertos funciona desde Android 8.
</details>

<details>
<summary><b>¿Funciona en dispositivos Samsung, Xiaomi y Pixel?</b></summary>
Sí. Incluye perfiles específicos optimizados para Samsung (One UI), Google Pixel (Stock) y Xiaomi (MIUI/HyperOS), con listas de paquetes protegidos y configuraciones adaptadas.
</details>

<details>
<summary><b>¿Cómo puedo contribuir al proyecto?</b></summary>
El proyecto es open source bajo licencia MIT. Puedes contribuir reportando bugs, creando nuevos módulos (plugins en Python), mejorando la documentación o enviando pull requests en GitHub.
</details>

---

## 📄 Licencia

Este proyecto está bajo la Licencia **MIT**. Consulta el archivo [LICENSE](LICENSE) para más detalles.

---

## 👤 Autor

**Ythan Javier Mora Gamarra**

<div align="center">

| Contacto | Enlace |
| :--- | :--- |
| 📧 Email | [ythanjavier6@gmail.com](mailto:ythanjavier6@gmail.com) |
| 📱 Teléfono | +593 991459589 |
| 💼 LinkedIn | [Ythan Javier](https://www.linkedin.com/in/ythan-javier-mora-gamarra/) |
| 💻 GitHub | [@JAVIER10733](https://github.com/JAVIER10733) |
| 📍 Ubicación | Ventanas, Los Ríos, Ecuador |

</div>

---

## 🌟 Agradecimientos

*   A la comunidad de **Termux** por mantener vivo el ecosistema de herramientas de terminal en Android.
*   A los creadores de **Rich**, **Bottle**, **pytest** y todas las librerías de código abierto que hacen esto posible.
*   A todos los **contribuidores** y **beta testers** que han ayudado a mejorar la herramienta.

<div align="center">

![Footer](https://capsule-render.vercel.app/api?type=waving&color=0:2c5364,50:19c3a6,100:0f2027&height=150&section=footer&text=Hecho%20con%20%E2%9D%A4%EF%B8%8F%20para%20la%20comunidad&fontSize=20&fontColor=ffffff&animation=twinkling)

</div>
