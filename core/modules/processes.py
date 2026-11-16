"""
Información de procesos del dispositivo.
"""

from typing import Any, Dict, List, Optional

from core.adb_wrapper import ADBWrapper
from core.logger import logger
from core.modules.base import BaseModule
from core.modules.registry import registry


@registry.register
class ProcessesModule(BaseModule):
    """Procesos en ejecución."""
    
    name = "processes"
    description = "Procesos en ejecución"
    requires_device = True
    requires_root = False
    danger_level = "low"
    
    def __init__(self, adb: Optional[ADBWrapper] = None) -> None:
        super().__init__(adb)
    
    def list_processes(self, filter_name: Optional[str] = None) -> List[Dict[str, str]]:
        """Lista procesos en ejecución."""
        self.require_device()
        
        try:
            output = self.adb.shell("ps -A")
        except Exception as e:
            logger.error(f"Error listando procesos: {e}")
            return []
        
        processes = []
        lines = output.strip().split('\n')
        
        if len(lines) < 2:
            return processes
        
        headers = lines[0].split()
        
        for line in lines[1:]:
            parts = line.split(None, len(headers) - 1)
            if len(parts) < len(headers):
                continue
            
            proc = dict(zip(headers, parts))
            
            if filter_name and filter_name.lower() not in proc.get("NAME", "").lower():
                continue
            
            processes.append(proc)
        
        return processes
    
    def execute(self, **kwargs) -> Any:
        filter_name = kwargs.get("filter")
        return self.list_processes(filter_name=filter_name)
    
    def print_processes(self, filter_name: Optional[str] = None) -> None:
        procs = self.list_processes(filter_name=filter_name)
        print(f"\n=== Procesos ({len(procs)}) ===")
        for p in procs[:50]:
            print(f"  {p.get('PID', 'N/A'):>8} {p.get('NAME', 'N/A')}")
        if len(procs) > 50:
            print(f"  ... y {len(procs) - 50} más")
        print()