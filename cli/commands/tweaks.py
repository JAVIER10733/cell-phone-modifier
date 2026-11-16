"""
Comandos de tweaks (placeholder para futuras funcionalidades).
"""

from cli.colors import print_info
from cli.ui import pause


class TweaksCommands:
    """Comandos de tweaks."""
    
    def run(self) -> None:
        """Menú de tweaks."""
        while True:
            print("\n=== Tweaks ===")
            print("⚠️  Módulo en desarrollo")
            print("0. Volver")
            
            from cli.ui import get_int_input
            choice = get_int_input("Tu elección", min_val=0, max_val=0)
            
            if choice is None or choice == 0:
                break
            
            pause()