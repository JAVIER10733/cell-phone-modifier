"""
Automatización y macros básicas.
"""

import time
from typing import Any, Dict, List, Optional

from core.adb_wrapper import ADBWrapper
from core.errors import ADBError
from core.logger import logger
from core.modules.base import BaseModule
from core.modules.registry import registry


@registry.register
class AutomationModule(BaseModule):
    """Automatización de tareas."""
    
    name = "automation"
    description = "Automatización y macros"
    requires_device = True
    requires_root = False
    danger_level = "medium"
    
    def __init__(self, adb: Optional[ADBWrapper] = None) -> None:
        super().__init__(adb)
        self._running = False
    
    def run_macro(self, steps: List[Dict[str, Any]]) -> None:
        """
        Ejecuta una macro (secuencia de acciones).
        
        Args:
            steps: Lista de pasos con formato:
                [{"action": "tap", "x": 100, "y": 200, "delay": 1}, ...]
        """
        self.require_device()
        self._running = True
        
        logger.info(f"Ejecutando macro con {len(steps)} pasos")
        
        for i, step in enumerate(steps, 1):
            if not self._running:
                logger.info("Macro detenida")
                break
            
            action = step.get("action")
            delay = step.get("delay", 0)
            
            logger.info(f"Paso {i}/{len(steps)}: {action}")
            
            try:
                if action == "tap":
                    self.adb.shell(f"input tap {step['x']} {step['y']}")
                elif action == "swipe":
                    self.adb.shell(
                        f"input swipe {step['x1']} {step['y1']} {step['x2']} {step['y2']}"
                    )
                elif action == "text":
                    self.adb.shell(f"input text '{step['text']}'")
                elif action == "key":
                    self.adb.shell(f"input keyevent {step['keycode']}")
                elif action == "wait":
                    time.sleep(step.get("seconds", 1))
            except Exception as e:
                logger.error(f"Error en paso {i}: {e}")
            
            if delay > 0:
                time.sleep(delay)
        
        self._running = False
        logger.info("Macro completada")
    
    def stop(self) -> None:
        """Detiene la macro en ejecución."""
        self._running = False
    
    def execute(self, action: str = "run", **kwargs) -> Any:
        if action == "run":
            return self.run_macro(kwargs.get("steps", []))
        elif action == "stop":
            return self.stop()
        return None