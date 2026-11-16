"""
Menú principal de cell_phone_modifier.
"""

from typing import Optional

from cli.banner import print_banner, print_menu_header
from cli.colors import print_error, print_info
from cli.ui import get_int_input, pause
from core.adb_wrapper import ADBWrapper
from core.dependencies import checker


class MainMenu:
    """Menú principal de la aplicación."""
    
    def __init__(self) -> None:
        self.adb = ADBWrapper()
        self._init_commands()
    
    def _init_commands(self) -> None:
        """Inicializa los comandos."""
        from cli.commands import (
            DeviceCommands,
            ConnectCommands,
            BackupCommands,
            AppsCommands,
            FilesCommands,
            DiagnosticsCommands,
            ConfigCommands,
        )
        from cli.commands.security import SecurityCommands
        from cli.commands.tweaks import TweaksCommands
        from cli.commands.automation import AutomationCommands
        
        self.device_cmd = DeviceCommands(self.adb)
        self.connect_cmd = ConnectCommands(self.adb)
        self.backup_cmd = BackupCommands(self.adb)
        self.apps_cmd = AppsCommands(self.adb)
        self.files_cmd = FilesCommands(self.adb)
        self.diagnostics_cmd = DiagnosticsCommands(self.adb)
        self.config_cmd = ConfigCommands()
        self.security_cmd = SecurityCommands()
        self.tweaks_cmd = TweaksCommands()
        self.automation_cmd = AutomationCommands()
    
    def show_status(self) -> None:
        """Muestra el estado actual."""
        devices = self.adb.get_devices()
        connected = [d for d in devices if d.get("state") == "device"]
        
        print("\n=== Estado ===")
        if self.adb.serial:
            print_info(f"Dispositivo seleccionado: {self.adb.serial}")
        elif connected:
            print_info(f"Dispositivos conectados: {len(connected)}")
        else:
            print_info("No hay dispositivos conectados")
    
    def show_main_menu(self) -> None:
        """Muestra el menú principal."""
        print_menu_header("Menú Principal")
        
        print("1. 📱 Dispositivo")
        print("2. 🔌 Conexión")
        print("3. 💾 Backup y Restauración")
        print("4. 📦 Aplicaciones")
        print("5. 📁 Archivos")
        print("6. 🔍 Diagnóstico")
        print("7. 🔒 Seguridad")
        print("8. ⚙️  Tweaks")
        print("9. 🤖 Automatización")
        print("10. ⚙️  Configuración")
        print("11. 📊 Estado del Sistema")
        print("0. 🚪 Salir")
    
    def show_system_status(self) -> None:
        """Muestra el estado del sistema."""
        from core.platform_utils import get_device_info
        
        info = get_device_info()
        
        print("\n=== Estado del Sistema ===")
        print(f"Plataforma: {info['platform']}")
        print(f"Arquitectura: {info['architecture']}")
        print(f"Python: {info['python_version']}")
        print(f"Termux: {'✅' if info['is_termux'] else '❌'}")
        print(f"Root: {'✅' if info['has_root'] else '❌'}")
        print(f"Almacenamiento: {'✅' if info['storage_accessible'] else '❌'}")
        
        print("\n=== Dependencias ===")
        checker.check_all()
        checker.print_status()
    
    def run(self) -> None:
        """Ejecuta el menú principal."""
        while True:
            print_banner()
            self.show_status()
            self.show_main_menu()
            
            choice = get_int_input("\nTu elección", min_val=0, max_val=11)
            
            if choice is None or choice == 0:
                print_info("¡Hasta luego!")
                break
            
            if choice == 1:
                self.device_cmd.run()
            elif choice == 2:
                self.connect_cmd.run()
            elif choice == 3:
                self.backup_cmd.run()
            elif choice == 4:
                self.apps_cmd.run()
            elif choice == 5:
                self.files_cmd.run()
            elif choice == 6:
                self.diagnostics_cmd.run()
            elif choice == 7:
                self.security_cmd.run()
            elif choice == 8:
                self.tweaks_cmd.run()
            elif choice == 9:
                self.automation_cmd.run()
            elif choice == 10:
                self.config_cmd.run()
            elif choice == 11:
                self.show_system_status()
                pause()