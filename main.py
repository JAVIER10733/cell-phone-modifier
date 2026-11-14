"""CPM - Entrypoint unificado (Web + CLI + TUI)."""

import sys
import os

# 🔥 FORZAR LA RUTA ABSOLUTA DEL PROYECTO 🔥
PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
if PROJECT_DIR not in sys.path:
    sys.path.insert(0, PROJECT_DIR)

import typer
from core.logger import configure_logger, get_logger
from core.config import load_config

config = load_config()
configure_logger(level=config.get("log_level", "INFO"))
log = get_logger(__name__)

app = typer.Typer(help="Cell Phone Modifier - Gestión Android")

try:
    from cli.commands import (
        device, apps, files, backup, security, 
        tweaks, flash, automation, diagnostics, config as config_cmd
    )
    app.add_typer(device.app, name="device")
    app.add_typer(apps.app, name="apps")
    app.add_typer(files.app, name="files")
    app.add_typer(backup.app, name="backup")
    app.add_typer(security.app, name="security")
    app.add_typer(tweaks.app, name="tweaks")
    app.add_typer(flash.app, name="flash")
    app.add_typer(automation.app, name="automation")
    app.add_typer(diagnostics.app, name="diagnostics")
    app.add_typer(config_cmd.app, name="config")
except ImportError as e:
    log.warning(f"No se pudieron cargar todos los comandos CLI: {e}")

def start_web():
    try:
        from web.server import app as flask_app
        port = config.get("dashboard_port", 8722)
        log.info(f"Iniciando Dashboard en http://127.0.0.1:{port}")
        print("===================================================")
        print(f"  CPM - DASHBOARD ACTIVO EN PUERTO {port}")
        print("  Presiona Ctrl+C para detener.")
        print("===================================================")
        flask_app.run(host="127.0.0.1", port=port, debug=False)
    except Exception as e:
        log.error(f"Error al iniciar el servidor: {e}")
        print(f"Error crítico: {e}")

def main():
    args = sys.argv[1:]
    if not args:
        start_web()
    elif args[0] == "web":
        start_web()
    elif args[0] == "--cli":
        from cli.menu import run_cli
        run_cli()
    elif args[0] == "--tui":
        from cli.tui.app import CpmTuiApp
        CpmTuiApp().run()
    else:
        app()

if __name__ == "__main__":
    main()
