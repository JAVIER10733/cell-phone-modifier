"""
Gestión de perfiles de dispositivo.
"""

import json
from pathlib import Path
from typing import Any, Dict, List, Optional

from core.errors import ConfigError
from core.logger import logger
from core.modules.base import BaseModule
from core.modules.registry import registry


@registry.register
class ProfilesModule(BaseModule):
    """Gestión de perfiles."""
    
    name = "profiles"
    description = "Perfiles de dispositivo"
    requires_device = False
    requires_root = False
    danger_level = "low"
    
    def __init__(self, profiles_dir: Optional[Path] = None) -> None:
        super().__init__()
        self.profiles_dir = profiles_dir or Path(__file__).parent.parent.parent / "config" / "profiles"
    
    def list_profiles(self) -> List[str]:
        """Lista perfiles disponibles."""
        if not self.profiles_dir.exists():
            return []
        
        return [
            f.stem for f in self.profiles_dir.glob("*.json")
        ]
    
    def load_profile(self, name: str) -> Dict[str, Any]:
        """Carga un perfil."""
        profile_file = self.profiles_dir / f"{name}.json"
        
        if not profile_file.exists():
            raise ConfigError(f"Perfil no encontrado: {name}")
        
        try:
            with open(profile_file, "r", encoding="utf-8") as f:
                return json.load(f)
        except json.JSONDecodeError as e:
            raise ConfigError(f"Error parseando perfil: {e}")
    
    def get_active_profile(self) -> Dict[str, Any]:
        """Obtiene el perfil activo desde config."""
        from core.config import config
        active = config.get("profiles.active", "default")
        return self.load_profile(active)
    
    def execute(self, action: str = "list", **kwargs) -> Any:
        if action == "list":
            return self.list_profiles()
        elif action == "load":
            return self.load_profile(kwargs.get("name", "default"))
        elif action == "active":
            return self.get_active_profile()
        return []