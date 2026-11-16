"""
Clase base para drivers de fabricantes.
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional

from core.adb_wrapper import ADBWrapper
from core.logger import logger


class BaseDriver(ABC):
    """Driver base para fabricantes."""
    
    brand: str = "generic"
    fastboot_mode_key: str = "vol_down + power"
    recovery_mode_key: str = "vol_up + power"
    
    def __init__(self, adb: Optional[ADBWrapper] = None) -> None:
        self.adb = adb or ADBWrapper()
    
    @abstractmethod
    def get_brand_info(self) -> Dict[str, Any]:
        """Obtiene información específica del fabricante."""
        pass
    
    def get_fastboot_instructions(self) -> str:
        """Instrucciones para entrar en fastboot."""
        return f"Apagar, luego {self.fastboot_mode_key}"
    
    def get_recovery_instructions(self) -> str:
        """Instrucciones para entrar en recovery."""
        return f"Apagar, luego {self.recovery_mode_key}"
    
    def get_known_issues(self) -> List[str]:
        """Lista de problemas conocidos del fabricante."""
        return []
    
    def get_safe_packages(self) -> List[str]:
        """Paquetes seguros de desactivar."""
        return []
    
    def get_protected_packages(self) -> List[str]:
        """Paquetes que NO se deben desactivar."""
        return []