"""
Comandos de gestión de archivos.
"""

from typing import Optional

from cli.colors import print_error, print_info, print_success
from cli.ui import confirm_action, get_input, pause
from core.adb_wrapper import ADBWrapper
from core.modules.files import FilesModule


class FilesCommands:
    """Comandos de gestión de archivos."""
    
    def __init__(self, adb: Optional[ADBWrapper] = None) -> None:
        self.adb = adb or ADBWrapper()
    
    def list_files(self) -> None:
        """Lista archivos en el dispositivo."""
        path = get_input("Ruta en dispositivo", default="/sdcard")
        if not path:
            return
        
        try:
            module = FilesModule(self.adb)
            module.print_list(path)
        except Exception as e:
            print_error(f"Error: {e}")
    
    def pull_file(self) -> None:
        """Copia archivo del dispositivo al PC."""
        remote = get_input("Ruta en dispositivo")
        if not remote:
            return
        
        local = get_input("Ruta local de destino")
        if not local:
            return
        
        try:
            module = FilesModule(self.adb)
            if module.pull_file(remote, local):
                print_success(f"Archivo copiado a: {local}")
            else:
                print_error("Error copiando archivo")
        except Exception as e:
            print_error(f"Error: {e}")
    
    def push_file(self) -> None:
        """Copia archivo del PC al dispositivo."""
        local = get_input("Ruta local del archivo")
        if not local:
            return
        
        remote = get_input("Ruta de destino en dispositivo")
        if not remote:
            return
        
        try:
            module = FilesModule(self.adb)
            if module.push_file(local, remote):
                print_success(f"Archivo copiado a: {remote}")
            else:
                print_error("Error copiando archivo")
        except Exception as e:
            print_error(f"Error: {e}")
    
    def delete_file(self) -> None:
        """Elimina archivo en el dispositivo."""
        path = get_input("Ruta del archivo a eliminar")
        if not path:
            return
        
        if not confirm_action(f"¿Eliminar {path}?", False):
            return
        
        try:
            module = FilesModule(self.adb)
            if module.delete_file(path):
                print_success("Archivo eliminado")
            else:
                print_error("Error eliminando archivo")
        except Exception as e:
            print_error(f"Error: {e}")
    
    def run(self) -> None:
        """Menú de gestión de archivos."""
        while True:
            print("\n=== Archivos ===")
            print("1. Listar archivos")
            print("2. Copiar del dispositivo (pull)")
            print("3. Copiar al dispositivo (push)")
            print("4. Eliminar archivo")
            print("0. Volver")
            
            from cli.ui import get_int_input
            choice = get_int_input("Tu elección", min_val=0, max_val=4)
            
            if choice is None or choice == 0:
                break
            
            if choice == 1:
                self.list_files()
            elif choice == 2:
                self.pull_file()
            elif choice == 3:
                self.push_file()
            elif choice == 4:
                self.delete_file()
            
            pause()