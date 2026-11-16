"""
Información de paquetes del sistema.
"""

from typing import Any, Dict, List, Optional

from core.adb_wrapper import ADBWrapper
from core.logger import logger
from core.modules.base import BaseModule
from core.modules.registry import registry


@registry.register
class PackagesModule(BaseModule):
    """Paquetes del sistema."""
    
    name = "packages"
    description = "Información de paquetes del sistema"
    requires_device = True
    requires_root = False
    danger_level = "low"
    
    def __init__(self, adb: Optional[ADBWrapper] = None) -> None:
        super().__init__(adb)
    
    def list_system_packages(self) -> List[str]:
        """Lista paquetes del sistema."""
        self.require_device()
        
        try:
            result = self.adb._execute(["shell", "pm", "list", "packages", "-s"])
            packages = []
            for line in result.stdout.strip().split('\n'):
                if line.startswith("package:"):
                    packages.append(line.replace("package:", "").strip())
            return sorted(packages)
        except Exception as e:
            logger.error(f"Error: {e}")
            return []
    
    def get_permissions(self, package: str) -> List[str]:
        """Obtiene permisos de un paquete."""
        self.require_device()
        
        try:
            output = self.adb.shell(f"dumpsys package {package} | grep permission")
            return [line.strip() for line in output.split('\n') if line.strip()]
        except Exception as e:
            logger.error(f"Error: {e}")
            return []
    
    def execute(self, action: str = "list_system", **kwargs) -> Any:
        if action == "list_system":
            return self.list_system_packages()
        elif action == "permissions":
            return self.get_permissions(kwargs.get("package", ""))
        return []