"""
Opciones de desarrollador y ADB WiFi.
"""

from typing import Any, Dict, Optional

from core.adb_wrapper import ADBWrapper
from core.logger import logger
from core.modules.base import BaseModule
from core.modules.registry import registry


@registry.register
class DeveloperModule(BaseModule):
    """Opciones de desarrollador."""
    
    name = "developer"
    description = "Opciones de desarrollador"
    requires_device = True
    requires_root = False
    danger_level = "medium"
    
    def __init__(self, adb: Optional[ADBWrapper] = None) -> None:
        super().__init__(adb)
    
    def get_developer_settings(self) -> Dict[str, str]:
        """Obtiene configuración de desarrollador."""
        self.require_device()
        
        settings = {}
        props = [
            "adb_enabled",
            "development_settings_enabled",
            "stay_on_while_plugged_in",
            "show_touches",
            "pointer_location",
        ]
        
        for prop in props:
            try:
                value = self.adb.shell(f"settings get global {prop}")
                settings[prop] = value
            except Exception:
                settings[prop] = "N/A"
        
        return settings
    
    def enable_adb_wifi(self, port: int = 5555) -> bool:
        """Activa ADB WiFi."""
        self.require_device()
        try:
            self.adb.shell(f"setprop service.adb.tcp.port {port}")
            self.adb.shell("stop adbd && start adbd")
            logger.info(f"ADB WiFi activado en puerto {port}")
            return True
        except Exception as e:
            logger.error(f"Error: {e}")
            return False
    
    def disable_adb_wifi(self) -> bool:
        """Desactiva ADB WiFi."""
        self.require_device()
        try:
            self.adb.shell("setprop service.adb.tcp.port -1")
            self.adb.shell("stop adbd && start adbd")
            logger.info("ADB WiFi desactivado")
            return True
        except Exception as e:
            logger.error(f"Error: {e}")
            return False
    
    def execute(self, action: str = "settings", **kwargs) -> Any:
        if action == "settings":
            return self.get_developer_settings()
        elif action == "enable_wifi":
            return self.enable_adb_wifi(kwargs.get("port", 5555))
        elif action == "disable_wifi":
            return self.disable_adb_wifi()
        return {}