"""
Diagnósticos del dispositivo.
"""

from typing import Any, Dict, Optional

from core.adb_wrapper import ADBWrapper
from core.logger import logger
from core.modules.base import BaseModule
from core.modules.registry import registry


@registry.register
class DiagnosticsModule(BaseModule):
    """Diagnósticos del dispositivo."""
    
    name = "diagnostics"
    description = "Diagnósticos del sistema"
    requires_device = True
    requires_root = False
    danger_level = "low"
    
    def __init__(self, adb: Optional[ADBWrapper] = None) -> None:
        super().__init__(adb)
    
    def run_diagnostics(self) -> Dict[str, Any]:
        """Ejecuta diagnósticos básicos."""
        self.require_device()
        
        results: Dict[str, Any] = {}
        
        # Sensores
        try:
            sensors = self.adb.shell("dumpsys sensorservice | grep 'Sensor'")
            results["sensors"] = len(sensors.split('\n')) if sensors else 0
        except Exception:
            results["sensors"] = "Error"
        
        # CPU info
        try:
            cpu = self.adb.shell("cat /proc/cpuinfo | grep 'Processor' | head -1")
            results["cpu"] = cpu
        except Exception:
            results["cpu"] = "N/A"
        
        # RAM
        try:
            meminfo = self.adb.shell("cat /proc/meminfo | grep 'MemTotal'")
            results["ram"] = meminfo
        except Exception:
            results["ram"] = "N/A"
        
        # Temperatura de batería
        try:
            temp = self.adb.shell("dumpsys battery | grep temperature")
            results["battery_temp"] = temp
        except Exception:
            results["battery_temp"] = "N/A"
        
        # Uptime
        try:
            uptime = self.adb.shell("cat /proc/uptime")
            results["uptime"] = uptime
        except Exception:
            results["uptime"] = "N/A"
        
        return results
    
    def execute(self, **kwargs) -> Any:
        return self.run_diagnostics()
    
    def print_diagnostics(self) -> None:
        info = self.run_diagnostics()
        print("\n=== Diagnósticos ===")
        for key, value in info.items():
            print(f"{key}: {value}")
        print()