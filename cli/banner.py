"""
Módulo de branding y UI para cell_phone_modifier.

Proporciona el banner principal de la aplicación y utilidades para
renderizar encabezados de menú de forma consistente en toda la CLI.

Autor: Ythan Javier Mora Gamarra
Licencia: MIT
"""

from __future__ import annotations

# ============================================================================
# CONSTANTES DE ESTILO (ANSI)
# ============================================================================

_RESET = "\033[0m"
_BOLD = "\033[1m"
_DIM = "\033[2m"
_CYAN = "\033[96m"
_GRAY = "\033[90m"
_WHITE = "\033[97m"
_GREEN = "\033[92m"
_YELLOW = "\033[93m"


# ============================================================================
# BANNER PRINCIPAL
# ============================================================================

BANNER = f"""{_CYAN}
╔══════════════════════════════════════════════════════════════════════════════════════════════╗
║                                                                                              ║
║   ██████╗███████╗██╗     ██╗     ██████╗ ██╗  ██╗ ██████╗ ███╗   ██╗███████╗                ║
║  ██╔════╝██╔════╝██║     ██║     ██╔══██╗██║  ██║██╔═══██╗████╗  ██║██╔════╝                ║
║  ██║     █████╗  ██║     ██║     ██████╔╝███████║██║   ██║██╔██╗ ██║█████╗                  ║
║  ██║     ██╔══╝  ██║     ██║     ██╔═══╝ ██╔══██║██║   ██║██║╚██╗██║██╔══╝                  ║
║  ╚██████╗███████╗███████╗███████╗██║     ██║  ██║╚██████╔╝██║ ╚████║███████╗                ║
║   ╚═════╝╚══════╝╚══════╝╚══════╝╚═╝     ╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═══╝╚══════╝                ║
║                                                                                              ║
║                            ███╗   ███╗ ██████╗ ██████╗ ██╗███████╗██╗███████╗██████╗          ║
║                            ████╗ ████║██╔═══██╗██╔══██╗██║██╔════╝██║██╔════╝██╔══██╗         ║
║                            ██╔████╔██║██║   ██║██║  ██║██║█████╗  ██║█████╗  ██████╔╝         ║
║                            ██║╚██╔╝██║██║   ██║██║  ██║██║██╔══╝  ██║██╔══╝  ██╔══██╗         ║
║                            ██║ ╚═╝ ██║╚██████╔╝██████╔╝██║██║     ██║███████╗██║  ██║         ║
║                            ╚═╝     ╚═╝ ╚═════╝ ╚═════╝ ╚═╝╚═╝     ╚═╝╚══════╝╚═╝  ╚═╝         ║
║                                                                                              ║
║   {_GRAY}┌──────────────────────────────────────────────────────────────────────────────────────┐{_CYAN}   ║
║   {_GRAY}│{_RESET}                                                                                      {_GRAY}│{_CYAN}   ║
║   {_GRAY}│{_WHITE}   ▸ {_CYAN}PROJECT    {_WHITE}cell_phone_modifier                                                {_GRAY}│{_CYAN}   ║
║   {_GRAY}│{_WHITE}   ▸ {_CYAN}EDITION    {_WHITE}Termux Edition                                                     {_GRAY}│{_CYAN}   ║
║   {_GRAY}│{_WHITE}   ▸ {_CYAN}VERSION    {_WHITE}v0.1.0  ·  Stable Channel                                          {_GRAY}│{_CYAN}   ║
║   {_GRAY}│{_WHITE}   ▸ {_CYAN}LICENSE    {_WHITE}MIT  ·  Open Source                                                {_GRAY}│{_CYAN}   ║
║   {_GRAY}│{_WHITE}   ▸ {_CYAN}PLATFORM   {_WHITE}Android 8.0+  ·  Linux (aarch64)                                   {_GRAY}│{_CYAN}   ║
║   {_GRAY}│{_WHITE}   ▸ {_CYAN}ENGINE     {_WHITE}Python 3.9+  ·  ADB Wireless                                       {_GRAY}│{_CYAN}   ║
║   {_GRAY}│{_WHITE}   ▸ {_CYAN}ROOT       {_WHITE}Not Required  ·  Zero Modifications                                {_GRAY}│{_CYAN}   ║
║   {_GRAY}│{_WHITE}   ▸ {_CYAN}MODULES    {_WHITE}20+ Production Ready                                               {_GRAY}│{_CYAN}   ║
║   {_GRAY}│{_RESET}                                                                                      {_GRAY}│{_CYAN}   ║
║   {_GRAY}└──────────────────────────────────────────────────────────────────────────────────────┘{_CYAN}   ║
║                                                                                              ║
║   {_GRAY}┌─────────────────────────────┬─────────────────────────────┬────────────────────────────┐{_CYAN} ║
║   {_GRAY}│{_WHITE}  {_BOLD}[ SYSTEM STATUS ]{_RESET}{_WHITE}          {_GRAY}│{_WHITE}  {_BOLD}[ SECURITY LAYER ]{_RESET}{_WHITE}         {_GRAY}│{_WHITE}  {_BOLD}[ CONNECTIVITY ]{_RESET}{_WHITE}          {_GRAY}│{_CYAN} ║
║   {_GRAY}├─────────────────────────────┼─────────────────────────────┼────────────────────────────┤{_CYAN} ║
║   {_GRAY}│{_WHITE}  Environment .... {_GREEN}TERMUX{_RESET}{_WHITE}    {_GRAY}│{_WHITE}  Telemetry ...... {_GREEN}DISABLED{_RESET}{_WHITE}  {_GRAY}│{_WHITE}  ADB Mode .... {_GREEN}WIRELESS{_RESET}{_WHITE}   {_GRAY}│{_CYAN} ║
║   {_GRAY}│{_WHITE}  Dependencies ... {_GREEN}OK{_RESET}{_WHITE}        {_GRAY}│{_WHITE}  Data Leak ...... {_GREEN}NONE{_RESET}{_WHITE}      {_GRAY}│{_WHITE}  Pairing ..... {_GREEN}READY{_RESET}{_WHITE}      {_GRAY}│{_CYAN} ║
║   {_GRAY}│{_WHITE}  Permissions .... {_GREEN}OK{_RESET}{_WHITE}        {_GRAY}│{_WHITE}  Audit Trail .... {_GREEN}ENABLED{_RESET}{_WHITE}   {_GRAY}│{_WHITE}  Latency ..... {_GREEN}OPTIMAL{_RESET}{_WHITE}    {_GRAY}│{_CYAN} ║
║   {_GRAY}└─────────────────────────────┴─────────────────────────────┴────────────────────────────┘{_CYAN} ║
║                                                                                              ║
║   {_GRAY}┌──────────────────────────────────────────────────────────────────────────────────────┐{_CYAN}   ║
║   {_GRAY}│{_RESET}                                                                                      {_GRAY}│{_CYAN}   ║
║   {_GRAY}│{_WHITE}   ▸ {_CYAN}AUTHOR     {_WHITE}Ythan Javier Mora Gamarra                                             {_GRAY}│{_CYAN}   ║
║   {_GRAY}│{_WHITE}   ▸ {_CYAN}REPO       {_WHITE}github.com/JAVIER10733/cell-phone-modifier                            {_GRAY}│{_CYAN}   ║
║   {_GRAY}│{_WHITE}   ▸ {_CYAN}COMMUNITY  {_WHITE}Termux  ·  F-Droid  ·  Open Source Contributors                       {_GRAY}│{_CYAN}   ║
║   {_GRAY}│{_WHITE}   ▸ {_CYAN}CONTACT    {_WHITE}Ventanas, Los Ríos, Ecuador  ·  2026                                  {_GRAY}│{_CYAN}   ║
║   {_GRAY}│{_RESET}                                                                                      {_GRAY}│{_CYAN}   ║
║   {_GRAY}└──────────────────────────────────────────────────────────────────────────────────────┘{_CYAN}   ║
║                                                                                              ║
║                     {_GREEN}► INITIALIZING PHONE MODIFIER RUNTIME · PLEASE WAIT ◄{_CYAN}                    ║
║                                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════════════════════╝{_RESET}
"""


# ============================================================================
# FUNCIONES PÚBLICAS
# ============================================================================

def print_banner() -> None:
    """Imprime el banner de la aplicación."""
    print(BANNER)


def print_menu_header(title: str, subtitle: str | None = None) -> None:
    """
    Imprime un encabezado de menú con formato profesional.

    Args:
        title: Título principal del menú.
        subtitle: Subtítulo opcional (ej. descripción breve).
    """
    width = 60
    inner = width - 2

    print(f"\n{_CYAN}╔{'═' * inner}╗{_RESET}")
    print(f"{_CYAN}║{_RESET} {_BOLD}{_WHITE}{title.center(inner - 2)}{_RESET} {_CYAN}║{_RESET}")
    if subtitle:
        print(f"{_CYAN}╟{'─' * inner}╢{_RESET}")
        print(f"{_CYAN}║{_RESET} {_DIM}{_GRAY}{subtitle.center(inner - 2)}{_RESET} {_CYAN}║{_RESET}")
    print(f"{_CYAN}╚{'═' * inner}╝{_RESET}\n")


def print_divider(label: str = "", char: str = "─", width: int = 60) -> None:
    """
    Imprime una línea divisoria opcional con etiqueta centrada.

    Args:
        label: Texto opcional a mostrar en el centro.
        char: Carácter usado para la línea.
        width: Ancho total de la línea.
    """
    if label:
        side = (width - len(label) - 2) // 2
        line = f"{char * side} {label} {char * side}"
        line = line[:width].ljust(width, char)
    else:
        line = char * width
    print(f"{_GRAY}{line}{_RESET}")


def print_status(label: str, value: str, ok: bool = True) -> None:
    """
    Imprime una línea de estado tipo `clave .... valor`.

    Args:
        label: Nombre del estado.
        value: Valor del estado.
        ok: Si es True, el valor se pinta en verde.
    """
    color = _GREEN if ok else _YELLOW
    print(f"  {_GRAY}{label:<20}{_RESET} {color}{value}{_RESET}")


# ============================================================================
# EJECUCIÓN DIRECTA (DEMO)
# ============================================================================

if __name__ == "__main__":
    print_banner()
    print_menu_header("MENÚ PRINCIPAL", "Selecciona una opción para continuar")
    print_status("Environment", "TERMUX")
    print_status("Dependencies", "OK")
    print_status("ADB Mode", "WIRELESS")
    print_divider("fin del demo")
