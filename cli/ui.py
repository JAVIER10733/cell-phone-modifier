"""
Utilidades de UI para la CLI.
Entradas, tablas, spinners y confirmaciones.
"""

from typing import Any, Callable, List, Optional, Tuple

from rich.prompt import Confirm, IntPrompt, Prompt
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TextColumn

from cli.colors import console, print_error, print_warning


def get_input(prompt: str, default: Optional[str] = None, password: bool = False) -> str:
    """
    Obtiene entrada del usuario.
    
    Args:
        prompt: Texto del prompt
        default: Valor por defecto
        password: Si True, oculta la entrada
    
    Returns:
        str: Entrada del usuario
    """
    try:
        return Prompt.ask(prompt, default=default, password=password)
    except (EOFError, KeyboardInterrupt):
        print("\n")
        return ""


def get_int_input(prompt: str, default: Optional[int] = None, min_val: Optional[int] = None, max_val: Optional[int] = None) -> Optional[int]:
    """
    Obtiene entrada numérica del usuario.
    
    Args:
        prompt: Texto del prompt
        default: Valor por defecto
        min_val: Valor mínimo
        max_val: Valor máximo
    
    Returns:
        Optional[int]: Número ingresado o None si se cancela
    """
    try:
        value = IntPrompt.ask(prompt, default=default)
        
        if min_val is not None and value < min_val:
            print_warning(f"Valor mínimo: {min_val}")
            return None
        
        if max_val is not None and value > max_val:
            print_warning(f"Valor máximo: {max_val}")
            return None
        
        return value
    except (EOFError, KeyboardInterrupt):
        print("\n")
        return None


def confirm_action(message: str, default: bool = False) -> bool:
    """
    Pide confirmación al usuario.
    
    Args:
        message: Mensaje de confirmación
        default: Valor por defecto
    
    Returns:
        bool: True si confirma
    """
    try:
        return Confirm.ask(message, default=default)
    except (EOFError, KeyboardInterrupt):
        print("\n")
        return False


def select_option(options: List[str], prompt: str = "Selecciona una opción") -> Optional[int]:
    """
    Muestra un menú de opciones y retorna el índice seleccionado.
    
    Args:
        options: Lista de opciones
        prompt: Texto del prompt
    
    Returns:
        Optional[int]: Índice seleccionado o None si se cancela
    """
    if not options:
        return None
    
    print(f"\n{prompt}:")
    for i, option in enumerate(options, 1):
        print(f"  {i}. {option}")
    print("  0. Cancelar")
    
    choice = get_int_input("Tu elección", min_val=0, max_val=len(options))
    
    if choice is None or choice == 0:
        return None
    
    return choice - 1


def show_table(title: str, headers: List[str], rows: List[List[str]]) -> None:
    """
    Muestra una tabla con Rich.
    
    Args:
        title: Título de la tabla
        headers: Encabezados de columnas
        rows: Filas de datos
    """
    table = Table(title=title, show_header=True, header_style="bold cyan")
    
    for header in headers:
        table.add_column(header)
    
    for row in rows:
        table.add_row(*row)
    
    console.print(table)


def show_progress(description: str) -> Progress:
    """
    Crea un spinner de progreso.
    
    Args:
        description: Descripción del progreso
    
    Returns:
        Progress: Objeto de progreso
    """
    return Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console,
        transient=True,
    )


def clear_screen() -> None:
    """Limpia la pantalla."""
    console.clear()


def pause(message: str = "Presiona Enter para continuar...") -> None:
    """Pausa la ejecución hasta que el usuario presione Enter."""
    try:
        input(f"\n{message}")
    except (EOFError, KeyboardInterrupt):
        print("\n")