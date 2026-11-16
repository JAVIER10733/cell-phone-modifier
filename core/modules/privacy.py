"""
Privacidad y permisos de apps.
"""

from typing import Any, Dict, List, Optional

from core.adb_wrapper import ADBWrapper
from core.logger import logger
from core.modules.base import BaseModule
from core.modules.registry import registry


@registry.register
class PrivacyModule(BaseModule):
    """Privacidad y permisos."""
    
    name = "privacy"
    description = "Privacidad y permisos"
    requires_device = True
    requires_root = False
    danger_level = "low"
    
    def __init__(self, adb: Optional[ADBWrapper] = None) -> None:
        super().__init__(adb)
    
    def get_app_permissions(self, package: str) -> List[str]:
        """Obtiene permisos de una app."""
        self.require_device()
        
        try:
            output = self.adb.shell(f"dumpsys package {package} | grep 'granted=true'")
            return [line.strip() for line in output.split('\n') if line.strip()]
        except Exception as e:
            logger.error(f"Error: {e}")
            return []
    
    def list_dangerous_permissions(self) -> Dict[str, List[str]]:
        """Lista permisos peligrosos concedidos."""
        self.require_device()
        
        dangerous_perms = [
            "CAMERA", "RECORD_AUDIO", "READ_CONTACTS", "WRITE_CONTACTS",
            "READ_SMS", "SEND_SMS", "ACCESS_FINE_LOCATION",
            "READ_PHONE_STATE", "READ_EXTERNAL_STORAGE",
            "WRITE_EXTERNAL_STORAGE", "READ_CALL_LOG"
        ]
        
        result: Dict[str, List[str]] = {perm: [] for perm in dangerous_perms}
        
        try:
            output = self.adb.shell("dumpsys package | grep 'granted=true'")
            for perm in dangerous_perms:
                for line in output.split('\n'):
                    if perm in line and "package:" in line:
                        pkg = line.split("package:")[1].strip() if "package:" in line else "unknown"
                        result[perm].append(pkg)
        except Exception as e:
            logger.error(f"Error: {e}")
        
        return result
    
    def execute(self, action: str = "dangerous_perms", **kwargs) -> Any:
        if action == "app_perms":
            return self.get_app_permissions(kwargs.get("package", ""))
        elif action == "dangerous_perms":
            return self.list_dangerous_permissions()
        return {}