"""
Paquete de comandos CLI.
"""

from cli.commands.device import DeviceCommands
from cli.commands.connect import ConnectCommands
from cli.commands.backup import BackupCommands
from cli.commands.apps import AppsCommands
from cli.commands.files import FilesCommands
from cli.commands.diagnostics import DiagnosticsCommands
from cli.commands.config import ConfigCommands

__all__ = [
    "DeviceCommands",
    "ConnectCommands",
    "BackupCommands",
    "AppsCommands",
    "FilesCommands",
    "DiagnosticsCommands",
    "ConfigCommands",
]