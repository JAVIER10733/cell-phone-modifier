#!/usr/bin/env python3
"""
cell_phone_modifier - Herramienta de modificación de dispositivos Android desde Termux.

Punto de entrada principal de la aplicación.
Ofrece CLI interactiva, dashboard web y ejecución de módulos individuales.

Autor: Ythan Javier Mora Gamarra
Versión: 0.1.0
"""

import sys
from pathlib import Path

# Asegurar que el directorio raíz esté en el path
sys.path.insert(0, str(Path(__file__).parent))

from cli.menu import MainMenu
from core.config import config
from core.dependencies import check_dependencies
from core.errors import CellPhoneModifierError, DependencyError, TermuxError
from core.logger import logger
from core.platform_utils import get_device_info, is_termux


def print_banner() -> None:
    """Imprime el banner de la aplicación."""
    banner = """
╔═══════════════════════════════════════════════════════════════╗
║                                                               ║
║   ██████╗███████╗██╗     ███████╗██╗      ██████╗            ║
║  ██╔════╝██╔════╝██║     ██╔════╝██║     ██╔═══██╗           ║
║  ██║     █████╗  ██║     █████╗  ██║     ██║   ██║           ║
║  ██║     ██╔══╝  ██║     ██╔══╝  ██║     ██║   ██║           ║
║  ╚██████╗███████╗███████╗██║     ███████╗╚██████╔╝           ║
║   ╚═════╝╚══════╝╚══════╝╚═╝     ╚══════╝ ╚═════╝            ║
║                                                               ║
║           PHONE MODIFIER - Termux Edition v0.1.0              ║
║                                                               ║
╚═══════════════════════════════════════════════════════════════╝
"""
    print(banner)


def print_device_info() -> None:
    """Imprime información del dispositivo."""
    info = get_device_info()
    print("\n=== Información del Dispositivo ===")
    print(f"Plataforma: {info['platform']}")
    print(f"Arquitectura: {info['architecture']}")
    print(f"Python: {info['python_version']}")
    print(f"Termux: {'✅' if info['is_termux'] else '❌'}")
    print(f"Root: {'✅' if info['has_root'] else '❌'}")
    print(f"Almacenamiento: {'✅' if info['storage_accessible'] else '❌'}")
    print()


def main() -> int:
    """
    Función principal de la aplicación.
    
    Returns:
        int: Código de salida (0 = éxito, 1 = error).
    """
    try:
        print_banner()
        
        # Verificar que estamos en Termux
        if not is_termux():
            logger.error("Este proyecto solo funciona en Termux.")
            print("\n❌ Error: Este proyecto solo funciona en Termux.")
            print("Instala Termux desde: https://f-droid.org/packages/com.termux/")
            return 1
        
        logger.info("Iniciando cell_phone_modifier en Termux")
        
        # Mostrar información del dispositivo
        print_device_info()
        
        # Verificar dependencias críticas
        logger.info("Verificando dependencias...")
        try:
            check_dependencies(required=["python", "adb"])
        except DependencyError as e:
            logger.error(f"Error de dependencias: {e}")
            print(f"\n❌ Error: {e}")
            print("\nPara instalar dependencias faltantes:")
            print("  pkg install python android-tools git")
            print("  pip install -r requirements.txt")
            return 1
        
        # Ejecutar menú principal
        menu = MainMenu()
        menu.run()
        
        logger.info("Aplicación cerrada correctamente")
        return 0
        
    except TermuxError as e:
        logger.error(f"Error de Termux: {e}")
        print(f"\n❌ Error de Termux: {e}")
        return 1
    except CellPhoneModifierError as e:
        logger.error(f"Error: {e}")
        print(f"\n❌ Error: {e}")
        return 1
    except KeyboardInterrupt:
        logger.info("Aplicación interrumpida por el usuario")
        print("\n\n⚠️  Aplicación interrumpida.")
        return 0
    except Exception as e:
        logger.exception(f"Error inesperado: {e}")
        print(f"\n❌ Error inesperado: {e}")
        print("Revisa logs/errors.log para más detalles.")
        return 1


if __name__ == "__main__":
    sys.exit(main())