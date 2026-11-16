"""
Gestión de SMS (requiere permisos especiales).
"""

from typing import Any, Dict, List, Optional

from core.adb_wrapper import ADBWrapper
from core.logger import logger
from core.modules.base import BaseModule
from core.modules.registry import registry


@registry.register
class SMSModule(BaseModule):
    """SMS del dispositivo."""
    
    name = "sms"
    description = "Gestión de SMS"
    requires_device = True
    requires_root = False
    danger_level = "medium"
    
    def __init__(self, adb: Optional[ADBWrapper] = None) -> None:
        super().__init__(adb)
    
    def list_sms(self, limit: int = 50) -> List[Dict[str, str]]:
        """Lista SMS recientes (puede requerir permisos)."""
        self.require_device()
        
        try:
            output = self.adb.shell(
                f"content query --uri content://sms/inbox --projection address:body:date --sort date DESC --limit {limit}"
            )
            
            messages = []
            for line in output.strip().split('\n'):
                if "address=" in line:
                    address = line.split("address=")[1].split(",")[0] if "address=" in line else "N/A"
                    body = line.split("body=")[1].split(",")[0] if "body=" in line else "N/A"
                    date = line.split("date=")[1].split(",")[0] if "date=" in line else "N/A"
                    messages.append({"from": address, "body": body, "date": date})
            
            return messages
        except Exception as e:
            logger.warning(f"SMS requieren permisos: {e}")
            return []
    
    def execute(self, **kwargs) -> Any:
         return self.list_sms(kwargs.get("limit", 50))