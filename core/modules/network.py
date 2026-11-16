"""
Información de red del dispositivo.
"""

from typing import Any, Dict, Optional

from core.adb_wrapper import ADBWrapper
from core.logger import logger
from core.modules.base import BaseModule
from core.modules.registry import registry


@registry.register
class NetworkModule(BaseModule):
    """Información de red."""
    
    name = "network"
    description = "Información de red (WiFi, celular)"
    requires_device = True
    requires_root = False
    danger_level = "low"
    
    def __init__(self, adb: Optional[ADBWrapper] = None) -> None:
        super().__init__(adb)
    
    def execute(self, **kwargs) -> Dict[str, Any]:
        self.require_device()
        
        info: Dict[str, Any] = {}
        
        # WiFi
        try:
            wifi_status = self.adb.shell("dumpsys wifi | grep 'mWifiInfo'")
            info["wifi_status"] = wifi_status
        except Exception as e:
            logger.debug(f"Error WiFi: {e}")
        
        # IP
        try:
            ip = self.adb.shell("ip addr show wlan0 | grep 'inet ' | awk '{print $2}' | cut -d/ -f1")
            info["wifi_ip"] = ip if ip else "No conectado"
        except Exception as e:
            logger.debug(f"Error IP: {e}")
        
        # Redes guardadas
        try:
            networks = self.adb.shell("dumpsys wifi | grep 'Configured networks' -A 100 | grep 'SSID:'")
            info["saved_networks"] = networks
        except Exception as e:
            logger.debug(f"Error redes guardadas: {e}")
        
        # Estado de datos móviles
        try:
            data_state = self.adb.shell("dumpsys telephony.registry | grep mDataConnectionState")
            info["mobile_data_state"] = data_state
        except Exception as e:
            logger.debug(f"Error datos móviles: {e}")
        
        return info
    
    def print_info(self) -> None:
        info = self.safe_execute()
        if not info:
            return
        
        print("\n=== Información de Red ===")
        print(f"WiFi IP:       {info.get('wifi_ip', 'N/A')}")
        print(f"WiFi Status:   {info.get('wifi_status', 'N/A')}")
        print(f"Datos Móviles: {info.get('mobile_data_state', 'N/A')}")
        print()