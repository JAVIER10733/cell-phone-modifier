"""
Comandos de dispositivo.
"""

from typing import Optional

from cli.colors import print_error, print_info, print_success
from cli.ui import pause, show_table
from core.adb_wrapper import ADBWrapper
from core.modules.device_info import DeviceInfoModule
from core.modules.battery import BatteryModule
from core.modules.storage import StorageModule


class DeviceCommands:
    """Comandos relacionados con el dispositivo."""
    
    def __init__(self, adb: Optional[ADBWrapper] = None) -> None:
        self.adb = adb or ADBWrapper()
    
    def list_devices(self) -> None:
        """Lista dispositivos conectados."""
        devices = self.adb.get_devices()
        
        if not devices:
            print_info("No hay dispositivos conectados")
            return
        
        headers = ["Serial", "Estado", "Modelo", "Producto"]
        rows = []
        
        for device in devices:
            serial = device.get("serial", "N/A")
            state = device.get("state", "N/A")
            model = device.get("model", "N/A")
            product = device.get("product", "N/A")
            rows.append([serial, state, model, product])
        
        show_table("Dispositivos Conectados", headers, rows)
    
    def show_device_info(self) -> None:
        """Muestra información completa del dispositivo."""
        try:
            module = DeviceInfoModule(self.adb)
            module.print_info()
        except Exception as e:
            print_error(f"Error: {e}")
    
    def show_battery_info(self) -> None:
        """Muestra información de la batería."""
        try:
            module = BatteryModule(self.adb)
            module.print_info()
        except Exception as e:
            print_error(f"Error: {e}")
    
    def show_storage_info(self) -> None:
        """Muestra información del almacenamiento."""
        try:
            module = StorageModule(self.adb)
            module.print_info()
        except Exception as e:
            print_error(f"Error: {e}")
    
    def reboot_device(self, mode: str = "") -> None:
        """Reinicia el dispositivo."""
        from cli.ui import confirm_action
        
        mode_text = {
            "": "normalmente",
            "bootloader": "a bootloader",
            "recovery": "a recovery",
        }.get(mode, mode)
        
        if not confirm_action(f"¿Reiniciar dispositivo {mode_text}?", False):
            print_info("Reinicio cancelado")
            return
        
        try:
            if self.adb.reboot(mode):
                print_success("Comando de reinicio enviado")
            else:
                print_error("Error al reiniciar")
        except Exception as e:
            print_error(f"Error: {e}")
    
    def run(self) -> None:
        """Menú de comandos de dispositivo."""
        while True:
            print("\n=== Dispositivo ===")
            print("1. Listar dispositivos")
            print("2. Información del dispositivo")
            print("3. Información de batería")
            print("4. Información de almacenamiento")
            print("5. Reiniciar dispositivo")
            print("6. Reiniciar a bootloader")
            print("7. Reiniciar a recovery")
            print("0. Volver")
            
            from cli.ui import get_int_input
            choice = get_int_input("Tu elección", min_val=0, max_val=7)
            
            if choice is None or choice == 0:
                break
            
            if choice == 1:
                self.list_devices()
            elif choice == 2:
                self.show_device_info()
            elif choice == 3:
                self.show_battery_info()
            elif choice == 4:
                self.show_storage_info()
            elif choice == 5:
                self.reboot_device("")
            elif choice == 6:
                self.reboot_device("bootloader")
            elif choice == 7:
                self.reboot_device("recovery")
            
            pause()