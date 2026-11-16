"""
Utilidades de plataforma para detectar Termux, arquitectura, root y rutas.
Todas las funciones verifican el entorno real antes de ejecutar acciones.
"""

import os
import platform
import shutil
import subprocess
from pathlib import Path
from typing import Optional, Tuple

from core.errors import TermuxError


def is_termux() -> bool:
    """
    Detecta si el script se está ejecutando en Termux.
    
    Returns:
        bool: True si está en Termux, False en caso contrario.
    """
    prefix = os.environ.get("PREFIX", "")
    return prefix == "/data/data/com.termux/files/usr"


def get_termux_paths() -> dict:
    """
    Obtiene las rutas principales de Termux.
    
    Returns:
        dict: Diccionario con HOME, PREFIX, y rutas de almacenamiento.
    
    Raises:
        TermuxError: Si no está en Termux.
    """
    if not is_termux():
        raise TermuxError("Este proyecto solo funciona en Termux.")
    
    home = os.environ.get("HOME", "/data/data/com.termux/files/home")
    prefix = os.environ.get("PREFIX", "/data/data/com.termux/files/usr")
    
    return {
        "home": Path(home),
        "prefix": Path(prefix),
        "storage": Path(home) / "storage",
        "shared": Path(home) / "storage" / "shared",
        "downloads": Path(home) / "storage" / "downloads",
    }


def get_architecture() -> str:
    """
    Detecta la arquitectura del dispositivo.
    
    Returns:
        str: Arquitectura (aarch64, armv7l, x86_64, etc.)
    """
    try:
        result = subprocess.run(
            ["uname", "-m"],
            capture_output=True,
            text=True,
            check=True,
            timeout=5
        )
        return result.stdout.strip()
    except (subprocess.SubprocessError, FileNotFoundError):
        return platform.machine()


def is_root_available() -> bool:
    """
    Detecta si el dispositivo tiene root disponible.
    
    Returns:
        bool: True si hay root, False en caso contrario.
    """
    # Verificar si su existe en rutas comunes
    su_paths = [
        "/system/bin/su",
        "/system/xbin/su",
        "/sbin/su",
        "/data/bin/su",
    ]
    
    for path in su_paths:
        if os.path.exists(path):
            return True
    
    # Verificar con which su
    if shutil.which("su"):
        return True
    
    return False


def require_root(action: str = "esta acción") -> None:
    """
    Verifica si hay root disponible y lanza error si no.
    
    Args:
        action: Descripción de la acción que requiere root.
    
    Raises:
        TermuxError: Si no hay root disponible.
    """
    if not is_root_available():
        raise TermuxError(
            f"{action.capitalize()} requiere root. "
            "Instala Magisk o una solución de root compatible."
        )


def check_storage_access() -> bool:
    """
    Verifica si el almacenamiento compartido está accesible.
    
    Returns:
        bool: True si el almacenamiento está accesible.
    """
    if not is_termux():
        return False
    
    paths = get_termux_paths()
    storage_path = paths["storage"]
    
    return storage_path.exists() and storage_path.is_dir()


def setup_storage() -> Tuple[bool, str]:
    """
    Ejecuta termux-setup-storage para acceder al almacenamiento compartido.
    
    Returns:
        Tuple[bool, str]: (éxito, mensaje)
    """
    if not is_termux():
        return False, "No está en Termux."
    
    if check_storage_access():
        return True, "El almacenamiento ya está configurado."
    
    try:
        # termux-setup-storage requiere interacción del usuario
        # Solo lo sugerimos, no lo ejecutamos automáticamente
        return False, (
            "Ejecuta 'termux-setup-storage' manualmente para acceder "
            "al almacenamiento compartido del dispositivo."
        )
    except Exception as e:
        return False, f"Error al configurar almacenamiento: {e}"


def get_device_info() -> dict:
    """
    Obtiene información básica del dispositivo.
    
    Returns:
        dict: Información del dispositivo (arquitectura, sistema, etc.)
    """
    return {
        "platform": platform.system(),
        "architecture": get_architecture(),
        "python_version": platform.python_version(),
        "is_termux": is_termux(),
        "has_root": is_root_available(),
        "storage_accessible": check_storage_access() if is_termux() else False,
    }