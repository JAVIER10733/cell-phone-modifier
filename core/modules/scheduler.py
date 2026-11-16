"""
Programación de tareas (limitado en Termux).
"""

import subprocess
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

from core.errors import TermuxError
from core.logger import logger
from core.modules.base import BaseModule
from core.modules.registry import registry
from core.platform_utils import is_termux


@registry.register
class SchedulerModule(BaseModule):
    """Programación de tareas."""
    
    name = "scheduler"
    description = "Tareas programadas"
    requires_device = False
    requires_root = False
    danger_level = "low"
    
    def __init__(self) -> None:
        super().__init__()
        self.jobs_file = Path(__file__).parent.parent.parent / "data" / "scheduled_jobs.json"
        self.jobs_file.parent.mkdir(parents=True, exist_ok=True)
    
    def schedule_at(self, command: str, time_str: str) -> bool:
        """
        Programa una tarea con 'at' (si está disponible).
        
        Args:
            command: Comando a ejecutar
            time_str: Hora en formato HH:MM
        
        Returns:
            bool: True si fue exitoso
        """
        if not is_termux():
            raise TermuxError("Solo disponible en Termux")
        
        try:
            result = subprocess.run(
                ["at", time_str],
                input=command,
                capture_output=True,
                text=True,
                check=False,
                timeout=10
            )
            
            if result.returncode == 0:
                logger.info(f"Tarea programada para {time_str}")
                return True
            
            logger.warning(f"'at' no disponible: {result.stderr}")
            return False
        except FileNotFoundError:
            logger.warning("Comando 'at' no instalado")
            return False
        except Exception as e:
            logger.error(f"Error programando: {e}")
            return False
    
    def list_jobs(self) -> List[Dict[str, Any]]:
        """Lista tareas programadas."""
        if not self.jobs_file.exists():
            return []
        
        import json
        try:
            with open(self.jobs_file, "r") as f:
                return json.load(f)
        except Exception:
            return []
    
    def execute(self, action: str = "list", **kwargs) -> Any:
        if action == "schedule":
            return self.schedule_at(
                kwargs.get("command", ""),
                kwargs.get("time", "")
            )
        elif action == "list":
            return self.list_jobs()
        return []