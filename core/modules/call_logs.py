"""
Registro de llamadas (requiere permisos especiales).
"""

from typing import Any, Dict, List, Optional

from core.adb_wrapper import ADBWrapper
from core.logger import logger
from core.modules.base import BaseModule
from core.modules.registry import registry


@registry.register
class CallLogsModule(BaseModule):
    """Registro de llamadas."""
    
    name = "call_logs"
    description = "Registro de llamadas"
    requires_device = True
    requires_root = False
    danger_level = "medium"
    
    def __init__(self, adb: Optional[ADBWrapper] = None) -> None:
        super().__init__(adb)
    
    def list_calls(self, limit: int = 50) -> List[Dict[str, str]]:
        """Lista llamadas recientes (puede requerir permisos)."""
        self.require_device()
        
        try:
            output = self.adb.shell(
                f"content query --uri content://call_log/calls --projection number:name:type:date --sort date DESC --limit {limit}"
            )
            
            calls = []
            type_map = {"1": "Entrante", "2": "Saliente", "3": "Perdida"}
            
            for line in output.strip().split('\n'):
                if "number=" in line:
                    number = line.split("number=")[1].split(",")[0]
                    name = line.split("name=")[1].split(",")[0] if "name=" in line else "Desconocido"
                    call_type = line.split("type=")[1].split(",")[0] if "type=" in line else "0"
                    date = line.split("date=")[1].split(",")[0] if "date=" in line else "N/A"
                    
                    calls.append({
                        "number": number,
                        "name": name,
                        "type": type_map.get(call_type, "Desconocido"),
                        "date": date
                    })
            
            return calls
        except Exception as e:
            logger.warning(f"Call logs requieren permisos: {e}")
            return []
     
    def execute(self, **kwargs) -> Any:
        return self.list_calls(kwargs.get("limit", 50))