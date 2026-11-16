"""
Control de entrada: tap, swipe, text, keyevent.
"""

from typing import Any, Optional

from core.adb_wrapper import ADBWrapper
from core.errors import ADBError, ValidationError
from core.logger import logger
from core.modules.base import BaseModule
from core.modules.registry import registry


@registry.register
class InputControlModule(BaseModule):
    """Control de entrada del dispositivo."""
    
    name = "input_control"
    description = "Control táctil y de teclado"
    requires_device = True
    requires_root = False
    danger_level = "medium"
    
    def __init__(self, adb: Optional[ADBWrapper] = None) -> None:
        super().__init__(adb)
    
    def tap(self, x: int, y: int) -> bool:
        """Toca una coordenada."""
        self.require_device()
        try:
            self.adb.shell(f"input tap {x} {y}")
            logger.info(f"Tap en ({x}, {y})")
            return True
        except Exception as e:
            raise ADBError(f"Error en tap: {e}")
    
    def swipe(self, x1: int, y1: int, x2: int, y2: int, duration_ms: int = 300) -> bool:
        """Desliza entre dos coordenadas."""
        self.require_device()
        try:
            self.adb.shell(f"input swipe {x1} {y1} {x2} {y2} {duration_ms}")
            logger.info(f"Swipe ({x1},{y1}) -> ({x2},{y2})")
            return True
        except Exception as e:
            raise ADBError(f"Error en swipe: {e}")
    
    def text(self, text: str) -> bool:
        """Escribe texto (solo ASCII)."""
        self.require_device()
        try:
            # Escapar caracteres especiales
            safe_text = text.replace(" ", "%s").replace("'", "\\'")
            self.adb.shell(f"input text '{safe_text}'")
            return True
        except Exception as e:
            raise ADBError(f"Error escribiendo texto: {e}")
    
    def keyevent(self, keycode: int) -> bool:
        """Envía un keycode (ej: 3=Home, 4=Back, 26=Power)."""
        self.require_device()
        try:
            self.adb.shell(f"input keyevent {keycode}")
            return True
        except Exception as e:
            raise ADBError(f"Error en keyevent: {e}")
    
    def press_home(self) -> bool:
        return self.keyevent(3)
    
    def press_back(self) -> bool:
        return self.keyevent(4)
    
    def press_power(self) -> bool:
        return self.keyevent(26)
    
    def press_menu(self) -> bool:
        return self.keyevent(82)
    
    def execute(self, action: str = "tap", **kwargs) -> Any:
        actions = {
            "tap": lambda: self.tap(kwargs["x"], kwargs["y"]),
            "swipe": lambda: self.swipe(
                kwargs["x1"], kwargs["y1"], kwargs["x2"], kwargs["y2"],
                kwargs.get("duration_ms", 300)
            ),
            "text": lambda: self.text(kwargs["text"]),
            "keyevent": lambda: self.keyevent(kwargs["keycode"]),
            "home": self.press_home,
            "back": self.press_back,
            "power": self.press_power,
        }
        
        if action not in actions:
            raise ADBError(f"Acción desconocida: {action}")
        
        return actions[action]()