"""
Banner ASCII de cell_phone_modifier.
"""

BANNER = """
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


def print_banner() -> None:
    """Imprime el banner de la aplicación."""
    print(BANNER)


def print_menu_header(title: str) -> None:
    """Imprime el encabezado de un menú."""
    print(f"\n{'='*60}")
    print(f"  {title}")
    print(f"{'='*60}\n")