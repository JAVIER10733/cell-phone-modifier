# 📋 Changelog - cell_phone_modifier

Todos los cambios notables en este proyecto se documentan aquí.

El formato está basado en [Keep a Changelog](https://keepachangelog.com/es/1.0.0/).

## [0.1.0] - 2026-11-16

### ✨ Añadido

#### Fase 1 - Setup y configuración base

- Detección de entorno Termux
- Sistema de configuración con JSON y .env
- Logger rotativo con niveles
- Verificación de dependencias (python, adb, fastboot, git)
- Utilidades de plataforma (arquitectura, root, almacenamiento)
- Sistema de excepciones personalizadas

#### Fase 2 - Wrappers y utilidades

- Wrapper de ADB con subprocess (sin shell=True)
- Wrapper de Fastboot
- Validadores (serial, IP, puerto, rutas)
- Sistema de reintentos con backoff exponencial
- Manager de seguridad (confirmaciones, dry-run)

#### Fase 3 - Módulos básicos

- `device_info`: Información completa del dispositivo
- `battery`: Estado de batería
- `storage`: Particiones y uso
- `apps`: Gestión de aplicaciones
- `files`: Gestión de archivos
- `screenshots`: Capturas y grabación
- `backup`: Backup de APKs y adb backup
- `restore`: Restauración de backups
- `logs`: Logcat y dmesg
- Registro central de módulos con decoradores

#### Fase 4 - CLI interactiva

- Menú principal con Rich
- Comandos de dispositivo, conexión, backup, apps, archivos
- Dashboard de diagnóstico
- Comandos de configuración
- Colores y tablas con Rich

#### Fase 5 - Dashboard web

- Servidor web con Bottle (compatible con Termux)
- API REST para todos los módulos
- Frontend HTML/CSS/JS responsive
- Auto-refresh cada 30 segundos

#### Fase 6 - Tests y documentación

- Tests unitarios con pytest y mocks
- Tests de integración para backup
- Fixtures para ADB y configuración
- Documentación completa (setup, módulos, CLI, seguridad, troubleshooting)

### 🔧 Técnico

- Base de datos SQLite para historial
- Bus de eventos interno
- Sistema de hooks before/after
- Registro de auditoría
- Soporte para plugins externos
- Drivers por fabricante (Samsung, Pixel, Xiaomi, Generic)
- 20+ módulos funcionales
- Perfiles por fabricante con bloatware conocido

### ⚠️ Limitaciones conocidas

- `adb backup` limitado en Android 12+
- Contactos/SMS/Call logs requieren permisos especiales
- `dmesg` puede requerir root
- Dashboard web sin autenticación robusta
- Fastboot solo informativo (no flasheo por seguridad)

---

## [0.0.1] - 2026-11-01

### ✨ Añadido

- Estructura inicial del proyecto
- Diseño de arquitectura
- Definición de fases
