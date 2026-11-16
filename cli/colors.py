"""
Colores y estilos para la CLI usando Rich.
"""

from rich.console import Console
from rich.theme import Theme

# Tema personalizado
custom_theme = Theme({
    "info": "cyan",
    "success": "green",
    "warning": "yellow",
    "error": "red bold",
    "critical": "red bold reverse",
})

# Console global
console = Console(theme=custom_theme)


def print_info(message: str) -> None:
    """Imprime mensaje informativo."""
    console.print(f"[info]ℹ️  {message}[/info]")


def print_success(message: str) -> None:
    """Imprime mensaje de éxito."""
    console.print(f"[success]✅ {message}[/success]")


def print_warning(message: str) -> None:
    """Imprime mensaje de advertencia."""
    console.print(f"[warning]⚠️  {message}[/warning]")


def print_error(message: str) -> None:
    """Imprime mensaje de error."""
    console.print(f"[error]❌ {message}[/error]")


def print_critical(message: str) -> None:
    """Imprime mensaje crítico."""
    console.print(f"[critical]💀 {message}[/critical]")


def print_status(label: str, value: str, status: str = "info") -> None:
    """Imprime un par label: value con color."""
    color_map = {
        "info": "cyan",
        "success": "green",
        "warning": "yellow",
        "error": "red",
    }
    color = color_map.get(status, "white")
    console.print(f"[bold]{label}:[/bold] [{color}]{value}[/{color}]")