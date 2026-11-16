"""
Comandos de diagnóstico.
"""

from typing import Optional

from cli.colors import print_error, print_info, print_success
from cli.ui import get_input, get_int_input, pause
from core.adb_wrapper import ADBWrapper
from core.modules.logs import LogsModule
from core.modules.screenshots import ScreenshotsModule


class DiagnosticsCommands:
    """Comandos de diagnóstico."""
    
    def __init__(self, adb: Optional[ADBWrapper] = None) -> None:
        self.adb = adb or ADBWrapper()
    
    def take_screenshot(self) -> None:
        """Toma captura de pantalla."""
        try:
            module = ScreenshotsModule(self.adb)
            path = module.take_screenshot()
            print_success(f"Captura guardada en: {path}")
        except Exception as e:
            print_error(f"Error: {e}")
    
    def view_logcat(self) -> None:
        """Muestra logcat."""
        lines = get_int_input("Número de líneas", default=50, min_val=1, max_val=1000)
        if lines is None:
            return
        
        try:
            module = LogsModule(self.adb)
            module.print_logcat(lines=lines)
        except Exception as e:
            print_error(f"Error: {e}")
    
    def save_logcat(self) -> None:
        """Guarda logcat en archivo."""
        try:
            module = LogsModule(self.adb)
            path = module.save_logcat()
            print_success(f"Logcat guardado en: {path}")
        except Exception as e:
            print_error(f"Error: {e}")
    
    def clear_logcat(self) -> None:
        """Limpia logcat."""
        try:
            module = LogsModule(self.adb)
            if module.clear_logcat():
                print_success("Logcat limpiado")
            else:
                print_error("Error limpiando logcat")
        except Exception as e:
            print_error(f"Error: {e}")
    
    def run(self) -> None:
        """Menú de diagnóstico."""
        while True:
            print("\n=== Diagnóstico ===")
            print("1. Tomar captura de pantalla")
            print("2. Ver logcat")
            print("3. Guardar logcat")
            print("4. Limpiar logcat")
            print("0. Volver")
            
            choice = get_int_input("Tu elección", min_val=0, max_val=4)
            
            if choice is None or choice == 0:
                break
            
            if choice == 1:
                self.take_screenshot()
            elif choice == 2:
                self.view_logcat()
            elif choice == 3:
                self.save_logcat()
            elif choice == 4:
                self.clear_logcat()
            
            pause()