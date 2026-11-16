"""
Comandos de gestión de aplicaciones.
"""

from typing import Optional

from cli.colors import print_error, print_info, print_success
from cli.ui import confirm_action, get_input, pause, show_table
from core.adb_wrapper import ADBWrapper
from core.modules.apps import AppsModule


class AppsCommands:
    """Comandos de gestión de aplicaciones."""
    
    def __init__(self, adb: Optional[ADBWrapper] = None) -> None:
        self.adb = adb or ADBWrapper()
    
    def list_apps(self, include_system: bool = False) -> None:
        """Lista aplicaciones instaladas."""
        try:
            module = AppsModule(self.adb)
            packages = module.list_packages(include_system=include_system)
            
            if not packages:
                print_info("No hay aplicaciones")
                return
            
            headers = ["#", "Paquete"]
            rows = [[str(i), pkg] for i, pkg in enumerate(packages, 1)]
            
            show_table(f"Aplicaciones ({len(packages)})", headers, rows)
        except Exception as e:
            print_error(f"Error: {e}")
    
    def app_info(self) -> None:
        """Muestra información de una app."""
        package = get_input("Nombre del paquete")
        if not package:
            return
        
        try:
            module = AppsModule(self.adb)
            info = module.get_package_info(package)
            
            if "error" in info:
                print_error(f"Error: {info['error']}")
                return
            
            print(f"\n=== Información de {package} ===")
            for key, value in info.items():
                print(f"{key}: {value}")
        except Exception as e:
            print_error(f"Error: {e}")
    
    def install_apk(self) -> None:
        """Instala una APK."""
        path = get_input("Ruta del APK")
        if not path:
            return
        
        if not confirm_action(f"¿Instalar {path}?", False):
            return
        
        try:
            module = AppsModule(self.adb)
            if module.execute(action="install", apk_path=path, replace=True):
                print_success("APK instalada")
            else:
                print_error("Error instalando APK")
        except Exception as e:
            print_error(f"Error: {e}")
    
    def uninstall_app(self) -> None:
        """Desinstala una app."""
        package = get_input("Nombre del paquete")
        if not package:
            return
        
        if not confirm_action(f"¿Desinstalar {package}?", False):
            return
        
        try:
            module = AppsModule(self.adb)
            if module.execute(action="uninstall", package=package):
                print_success(f"{package} desinstalada")
            else:
                print_error("Error desinstalando")
        except Exception as e:
            print_error(f"Error: {e}")
    
    def run(self) -> None:
        """Menú de gestión de aplicaciones."""
        while True:
            print("\n=== Aplicaciones ===")
            print("1. Listar apps de usuario")
            print("2. Listar todas las apps (incluye sistema)")
            print("3. Información de una app")
            print("4. Instalar APK")
            print("5. Desinstalar app")
            print("0. Volver")
            
            from cli.ui import get_int_input
            choice = get_int_input("Tu elección", min_val=0, max_val=5)
            
            if choice is None or choice == 0:
                break
            
            if choice == 1:
                self.list_apps(include_system=False)
            elif choice == 2:
                self.list_apps(include_system=True)
            elif choice == 3:
                self.app_info()
            elif choice == 4:
                self.install_apk()
            elif choice == 5:
                self.uninstall_app()
            
            pause()