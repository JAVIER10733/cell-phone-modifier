"""
Comandos de backup y restauración.
"""

from typing import Optional

from cli.colors import print_error, print_info, print_success
from cli.ui import confirm_action, get_input, pause
from core.adb_wrapper import ADBWrapper
from core.modules.backup import BackupModule
from core.modules.restore import RestoreModule


class BackupCommands:
    """Comandos de backup y restauración."""
    
    def __init__(self, adb: Optional[ADBWrapper] = None) -> None:
        self.adb = adb or ADBWrapper()
    
    def backup_single_apk(self) -> None:
        """Backup de un APK específico."""
        package = get_input("Nombre del paquete (ej: com.whatsapp)")
        if not package:
            return
        
        try:
            module = BackupModule(self.adb)
            path = module.backup_apk(package)
            print_success(f"APK guardado en: {path}")
        except Exception as e:
            print_error(f"Error: {e}")
    
    def backup_all_apks(self) -> None:
        """Backup de todos los APKs."""
        if not confirm_action("¿Hacer backup de todos los APKs?", False):
            return
        
        try:
            module = BackupModule(self.adb)
            paths = module.backup_all_apks()
            print_success(f"{len(paths)} APKs guardados")
        except Exception as e:
            print_error(f"Error: {e}")
    
    def backup_full(self) -> None:
        """Backup completo con adb backup."""
        print_warning("adb backup está limitado en Android 12+")
        print_warning("Muchas apps no permiten backup de datos")
        
        if not confirm_action("¿Continuar con backup completo?", False):
            return
        
        try:
            module = BackupModule(self.adb)
            path = module.adb_backup()
            print_success(f"Backup guardado en: {path}")
        except Exception as e:
            print_error(f"Error: {e}")
    
    def restore_apk(self) -> None:
        """Restaurar un APK."""
        path = get_input("Ruta del APK")
        if not path:
            return
        
        if not confirm_action(f"¿Instalar {path}?", False):
            return
        
        try:
            module = RestoreModule(self.adb)
            if module.restore_apk(path):
                print_success("APK instalado")
            else:
                print_error("Error instalando APK")
        except Exception as e:
            print_error(f"Error: {e}")
    
    def restore_full(self) -> None:
        """Restaurar backup completo."""
        path = get_input("Ruta del archivo .ab")
        if not path:
            return
        
        if not confirm_action("¿Restaurar backup completo? Esto puede sobreescribir datos", False):
            return
        
        try:
            module = RestoreModule(self.adb)
            if module.adb_restore(path):
                print_success("Backup restaurado")
            else:
                print_error("Error restaurando backup")
        except Exception as e:
            print_error(f"Error: {e}")
    
    def run(self) -> None:
        """Menú de backup y restauración."""
        while True:
            print("\n=== Backup y Restauración ===")
            print("1. Backup de un APK")
            print("2. Backup de todos los APKs")
            print("3. Backup completo (adb backup)")
            print("4. Restaurar APK")
            print("5. Restaurar backup completo")
            print("0. Volver")
            
            from cli.ui import get_int_input
            choice = get_int_input("Tu elección", min_val=0, max_val=5)
            
            if choice is None or choice == 0:
                break
            
            if choice == 1:
                self.backup_single_apk()
            elif choice == 2:
                self.backup_all_apks()
            elif choice == 3:
                self.backup_full()
            elif choice == 4:
                self.restore_apk()
            elif choice == 5:
                self.restore_full()
            
            pause()