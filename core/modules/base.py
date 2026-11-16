"""
Clase base para todos los módulos de cell_phone_modifier.
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional

from core.adb_wrapper import ADBWrapper
from core.errors import CellPhoneModifierError, DeviceError
from core.logger import logger
from core.safety import safety


class BaseModule(ABC):
    """Clase base abstracta para todos los módulos."""
    
    name: str = "base"
    description: str = "Módulo base"
    requires_device: bool = True
    requires_root: bool = False
    danger_level: str = "low"
    
    def __init__(self, adb: Optional[ADBWrapper] = None) -> None:
        self.adb = adb or ADBWrapper()
        self._device_verified = False
    
    def verify_device(self) -> bool:
        if self._device_verified and self.adb.serial:
            if self.adb.is_device_connected():
                return True
        
        devices = self.adb.get_devices()
        connected = [d for d in devices if d.get("state") == "device"]
        
        if not connected:
            if not devices:
                raise DeviceError("No hay dispositivos conectados.")
            
            unauthorized = [d for d in devices if d.get("state") == "unauthorized"]
            if unauthorized:
                raise DeviceError("Dispositivo no autorizado. Acepta la solicitud de depuración USB.")
            
            raise DeviceError(f"No hay dispositivos autorizados. Estados: {[d.get('state') for d in devices]}")
        
        if not self.adb.serial and len(connected) == 1:
            self.adb.set_serial(connected[0]["serial"])
        
        self._device_verified = True
        return True
    
    def require_device(self) -> None:
        if self.requires_device:
            self.verify_device()
    
    @abstractmethod
    def execute(self, **kwargs) -> Any:
        pass
    
    def get_info(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "description": self.description,
            "requires_device": self.requires_device,
            "requires_root": self.requires_root,
            "danger_level": self.danger_level,
        }
    
    def safe_execute(self, **kwargs) -> Any:
        try:
            logger.info(f"Ejecutando módulo: {self.name}")
            
            if self.requires_device:
                self.require_device()
            
            if self.danger_level in ("high", "critical"):
                action = f"{self.name}: {self.description}"
                if self.danger_level == "critical":
                    if not safety.confirm_critical(action):
                        logger.info(f"Acción crítica cancelada: {self.name}")
                        return None
                else:
                    if not safety.confirm(action, self.danger_level):
                        logger.info(f"Acción cancelada: {self.name}")
                        return None
            
            return self.execute(**kwargs)
        
        except CellPhoneModifierError as e:
            logger.error(f"Error en módulo {self.name}: {e}")
            raise
        except Exception as e:
            logger.exception(f"Error inesperado en módulo {self.name}: {e}")
            raise CellPhoneModifierError(f"Error en {self.name}: {e}")