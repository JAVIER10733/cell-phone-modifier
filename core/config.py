"""
Módulo de configuración para cell_phone_modifier.
Carga configuración desde config.json y variables de entorno desde .env.
"""

import json
import os
from pathlib import Path
from typing import Any, Dict, Optional

from dotenv import load_dotenv

from core.errors import ConfigError


class Config:
    """
    Clase para manejar la configuración de la aplicación.
    Carga config.json y variables de entorno.
    """
    
    def __init__(self, config_dir: Optional[Path] = None) -> None:
        """
        Inicializa la configuración.
        
        Args:
            config_dir: Directorio donde está config.json. Si es None, usa config/.
        """
        self.config_dir = config_dir or Path(__file__).parent.parent / "config"
        self._config: Dict[str, Any] = {}
        self._load_env()
        self._load_config()
    
    def _load_env(self) -> None:
        """Carga variables de entorno desde .env."""
        env_file = Path(__file__).parent.parent / ".env"
        if env_file.exists():
            load_dotenv(env_file)
    
    def _load_config(self) -> None:
        """Carga configuración desde config.json."""
        config_file = self.config_dir / "config.json"
        
        if not config_file.exists():
            # Crear configuración por defecto si no existe
            self._config = self._default_config()
            self._save_config()
            return
        
        try:
            with open(config_file, "r", encoding="utf-8") as f:
                self._config = json.load(f)
        except json.JSONDecodeError as e:
            raise ConfigError(f"Error al parsear config.json: {e}")
        except Exception as e:
            raise ConfigError(f"Error al cargar config.json: {e}")
    
    def _default_config(self) -> Dict[str, Any]:
        """Retorna la configuración por defecto."""
        return {
            "app": {
                "name": "cell_phone_modifier",
                "version": "0.1.0",
                "debug": False,
            },
            "adb": {
                "timeout": 30,
                "retry_attempts": 3,
                "retry_delay": 2,
            },
            "backup": {
                "default_path": "~/storage/downloads/cell_phone_modifier/backups",
                "compress": True,
            },
            "logging": {
                "level": "INFO",
                "max_size_mb": 10,
                "backup_count": 5,
            },
        }
    
    def _save_config(self) -> None:
        """Guarda la configuración actual en config.json."""
        self.config_dir.mkdir(parents=True, exist_ok=True)
        config_file = self.config_dir / "config.json"
        
        try:
            with open(config_file, "w", encoding="utf-8") as f:
                json.dump(self._config, f, indent=2, ensure_ascii=False)
        except Exception as e:
            raise ConfigError(f"Error al guardar config.json: {e}")
    
    def get(self, key: str, default: Any = None) -> Any:
        """
        Obtiene un valor de la configuración usando notación de puntos.
        
        Args:
            key: Clave en formato "seccion.subseccion.valor"
            default: Valor por defecto si no existe.
        
        Returns:
            Valor de la configuración o default.
        """
        keys = key.split(".")
        value = self._config
        
        try:
            for k in keys:
                value = value[k]
            return value
        except (KeyError, TypeError):
            return default
    
    def set(self, key: str, value: Any) -> None:
        """
        Establece un valor en la configuración usando notación de puntos.
        
        Args:
            key: Clave en formato "seccion.subseccion.valor"
            value: Valor a establecer.
        """
        keys = key.split(".")
        config = self._config
        
        for k in keys[:-1]:
            if k not in config:
                config[k] = {}
            config = config[k]
        
        config[keys[-1]] = value
        self._save_config()
    
    def get_env(self, key: str, default: Optional[str] = None) -> Optional[str]:
        """
        Obtiene una variable de entorno.
        
        Args:
            key: Nombre de la variable de entorno.
            default: Valor por defecto si no existe.
        
        Returns:
            Valor de la variable de entorno o default.
        """
        return os.environ.get(key, default)
    
    def to_dict(self) -> Dict[str, Any]:
        """Retorna toda la configuración como diccionario."""
        return self._config.copy()


# Instancia global de configuración
config = Config()