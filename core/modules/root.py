"""
Detección de root y Magisk (solo lectura).
"""

from typing import Any, Dict, Optional

from core.adb_wrapper import ADBWrapper
from core.logger import logger
from core.modules.base import BaseModule
from core.modules.registry import registry
from core.platform_utils import is_root_available


@registry.register
class RootModule(BaseModule):
    """Detección de root."""
    
    name = "root"
    description = "Detección de root y Magisk"
    requires_device = True
    requires_root = False
    danger_level = "low"
    
    def __init__(self, adb: Optional[ADBWrapper] = None) -> None:
        super().__init__(adb)
    
    def detect_root(self) -> Dict[str, Any]:
        """Detecta si el dispositivo tiene root."""
        self.require_device()
        
        info: Dict[str, Any] = {
            "has_root": False,
            "root_method": None,
            "magisk_version": None,
            "selinux": None,
        }
        
        # Verificar su
        try:
            result = self.adb.shell("which su")
            if result and "su" in result:
                info["has_root"] = True
                info["root_method"] = "su binary"
        except Exception:
            pass
        
        # Verificar Magisk
        try:
            magisk = self.adb.shell("magisk -v")
            if magisk and not "not found" in magisk.lower():
                info["has_root"] = True
                info["root_method"] = "Magisk"
                info["magisk_version"] = magisk
        except Exception:
            pass
        
        # Verificar SELinux
        try:
            selinux = self.adb.shell("getenforce")
            info["selinux"] = selinux
        except Exception:
            pass
        
        # Verificar estado de Knox (Samsung)
        try:
            knox = self.adb.shell("getprop ro.boot.warranty_bit")
            if knox:
                info["knox_status"] = knox
        except Exception:
            pass
        
        return info
    
    def execute(self, **kwargs) -> Any:
        return self.detect_root()
    
    def print_info(self) -> None:
        info = self.detect_root()
        print("\n=== Estado de Root ===")
        print(f"Root:           {'✅' if info['has_root'] else '❌'}")
        print(f"Método:         {info.get('root_method', 'N/A')}")
        print(f"Magisk:         {info.get('magisk_version', 'N/A')}")
        print(f"SELinux:        {info.get('selinux', 'N/A')}")
        print(f"Knox:           {info.get('knox_status', 'N/A')}")
        print()