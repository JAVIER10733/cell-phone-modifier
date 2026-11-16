"""
Módulo de logging para cell_phone_modifier.
Configura logging rotativo en el directorio logs/.
"""

import logging
import logging.handlers
from pathlib import Path
from typing import Optional

from core.config import config
from core.platform_utils import get_termux_paths, is_termux


def get_log_dir() -> Path:
    """
    Obtiene el directorio de logs.
    
    Returns:
        Path: Ruta al directorio de logs.
    """
    if is_termux():
        paths = get_termux_paths()
        log_dir = paths["home"] / "cell_phone_modifier" / "logs"
    else:
        log_dir = Path(__file__).parent.parent / "logs"
    
    log_dir.mkdir(parents=True, exist_ok=True)
    return log_dir


def setup_logger(
    name: str = "cell_phone_modifier",
    level: Optional[str] = None,
    log_file: Optional[str] = None
) -> logging.Logger:
    """
    Configura y retorna un logger con rotación de archivos.
    
    Args:
        name: Nombre del logger.
        level: Nivel de logging (DEBUG, INFO, WARNING, ERROR, CRITICAL).
        log_file: Nombre del archivo de log. Si es None, usa app.log.
    
    Returns:
        logging.Logger: Logger configurado.
    """
    if level is None:
        level = config.get("logging.level", "INFO")
    
    if log_file is None:
        log_file = "app.log"
    
    log_dir = get_log_dir()
    log_path = log_dir / log_file
    
    # Obtener configuración de rotación
    max_size_mb = config.get("logging.max_size_mb", 10)
    backup_count = config.get("logging.backup_count", 5)
    
    # Crear logger
    logger = logging.getLogger(name)
    logger.setLevel(getattr(logging, level.upper()))
    
    # Evitar agregar handlers duplicados
    if logger.handlers:
        return logger
    
    # Formato del log
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )
    
    # Handler para archivo con rotación
    file_handler = logging.handlers.RotatingFileHandler(
        log_path,
        maxBytes=max_size_mb * 1024 * 1024,
        backupCount=backup_count,
        encoding="utf-8"
    )
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    
    # Handler para consola
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    return logger


# Logger global
logger = setup_logger()