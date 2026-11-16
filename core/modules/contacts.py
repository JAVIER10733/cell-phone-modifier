"""
Gestión de contactos (requiere permisos especiales).
"""

from typing import Any, Dict, List, Optional

from core.adb_wrapper import ADBWrapper
from core.logger import logger
from core.modules.base import BaseModule
from core.modules.registry import registry


@registry.register
class ContactsModule(BaseModule):
    """Contactos del dispositivo."""
    
    name = "contacts"
    description = "Gestión de contactos"
    requires_device = True
    requires_root = False
    danger_level = "medium"
    
    def __init__(self, adb: Optional[ADBWrapper] = None) -> None:
        super().__init__(adb)
    
    def list_contacts(self, limit: int = 100) -> List[Dict[str, str]]:
        """Lista contactos (puede requerir permisos)."""
        self.require_device()
        
        try:
            output = self.adb.shell(
                f"content query --uri content://contacts/phones --projection display_name:number --limit {limit}"
            )
            
            contacts = []
            for line in output.strip().split('\n'):
                if "display_name=" in line and "number=" in line:
                    name = line.split("display_name=")[1].split(",")[0] if "display_name=" in line else "N/A"
                    number = line.split("number=")[1].split(",")[0] if "number=" in line else "N/A"
                    contacts.append({"name": name, "number": number})
            
            return contacts
        except Exception as e:
            logger.warning(f"Contactos requieren permisos: {e}")
            return []
    
    def execute(self, **kwargs) -> Any:
        return self.list_contacts(kwargs.get("limit", 100))
    
    def print_contacts(self, limit: int = 50) -> None:
        contacts = self.list_contacts(limit=limit)
        print(f"\n=== Contactos ({len(contacts)}) ===")
        for c in contacts:
            print(f"  {c.get('name', 'N/A'):<30} {c.get('number', 'N/A')}")
        print()