"""
Comandos de automatización (placeholder para futuras funcionalidades).
"""

from cli.colors import print_info
from cli.ui import pause


class AutomationCommands:
    """Comandos de automatización."""
    
    def run(self) -> None:
        """Menú de automatización."""
        while True:
            print("\n=== Automatización ===")
            print("⚠️  Módulo en desarrollo")
            print("0. Volver")
            
            from cli.ui import get_int_input
            choice = get_int_input("Tu elección", min_val=0, max_val=0)
            
            if choice is None or choice == 0:
                break
            
            pause()