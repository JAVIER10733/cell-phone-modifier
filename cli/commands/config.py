"""
Comandos de configuración.
"""

from cli.colors import print_error, print_info, print_success
from cli.ui import get_input, pause, show_table
from core.config import config


class ConfigCommands:
    """Comandos de configuración."""
    
    def show_config(self) -> None:
        """Muestra la configuración actual."""
        cfg = config.to_dict()
        
        headers = ["Clave", "Valor"]
        rows = []
        
        def flatten_dict(d, parent_key=""):
            items = []
            for k, v in d.items():
                new_key = f"{parent_key}.{k}" if parent_key else k
                if isinstance(v, dict):
                    items.extend(flatten_dict(v, new_key))
                else:
                    items.append([new_key, str(v)])
            return items
        
        rows = flatten_dict(cfg)
        show_table("Configuración Actual", headers, rows)
    
    def set_config(self) -> None:
        """Establece un valor de configuración."""
        key = get_input("Clave (ej: adb.timeout)")
        if not key:
            return
        
        value = get_input("Valor")
        if not value:
            return
        
        # Intentar convertir a tipo apropiado
        try:
            if value.lower() in ("true", "false"):
                value = value.lower() == "true"
            elif value.isdigit():
                value = int(value)
            elif value.replace(".", "").isdigit():
                value = float(value)
        except Exception:
            pass
        
        try:
            config.set(key, value)
            print_success(f"{key} = {value}")
        except Exception as e:
            print_error(f"Error: {e}")
    
    def run(self) -> None:
        """Menú de configuración."""
        while True:
            print("\n=== Configuración ===")
            print("1. Ver configuración")
            print("2. Establecer valor")
            print("0. Volver")
            
            from cli.ui import get_int_input
            choice = get_int_input("Tu elección", min_val=0, max_val=2)
            
            if choice is None or choice == 0:
                break
            
            if choice == 1:
                self.show_config()
            elif choice == 2:
                self.set_config()
            
            pause()