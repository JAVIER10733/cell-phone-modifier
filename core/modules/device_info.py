"""
Módulo de información del dispositivo.
Obtiene datos del dispositivo Android conectado.
"""

from typing import Any, Dict, Optional

from core.adb_wrapper import ADBWrapper
from core.logger import logger
from core.modules.base import BaseModule
from core.modules.registry import registry


@registry.register
class DeviceInfoModule(BaseModule):
    """Obtiene información completa del dispositivo."""
    
    name = "device_info"
    description = "Información del dispositivo Android"
    requires_device = True
    requires_root = False
    danger_level = "low"
    
    def __init__(self, adb: Optional[ADBWrapper] = None) -> None:
        super().__init__(adb)
    
    def _get_prop(self, prop: str) -> str:
        """Obtiene una propiedad del dispositivo."""
        try:
            return self.adb.get_property(prop)
        except Exception as e:
            logger.debug(f"Error obteniendo {prop}: {e}")
            return "N/A"
    
    def execute(self, **kwargs) -> Dict[str, Any]:
        """
        Obtiene información completa del dispositivo.
        
        Returns:
            Dict[str, Any]: Información del dispositivo
        """
        self.require_device()
        
        info = {
            "serial": self.adb.serial,
            "model": self._get_prop("ro.product.model"),
            "brand": self._get_prop("ro.product.brand"),
            "manufacturer": self._get_prop("ro.product.manufacturer"),
            "android_version": self._get_prop("ro.build.version.release"),
            "sdk_version": self._get_prop("ro.build.version.sdk"),
            "build_id": self._get_prop("ro.build.id"),
            "build_type": self._get_prop("ro.build.type"),
            "security_patch": self._get_prop("ro.build.version.security_patch"),
            "cpu_abi": self._get_prop("ro.product.cpu.abi"),
            "hardware": self._get_prop("ro.hardware"),
            "board": self._get_prop("ro.product.board"),
            "device_name": self._get_prop("ro.product.device"),
        }
        
        # Información adicional vía shell
        try:
            info["resolution"] = self.adb.shell("wm size").replace("Physical size: ", "")
            info["density"] = self.adb.shell("wm density").replace("Physical density: ", "")
        except Exception as e:
            logger.debug(f"Error obteniendo resolución/densidad: {e}")
            info["resolution"] = "N/A"
            info["density"] = "N/A"
        
        # Uptime
        try:
            uptime_raw = self.adb.shell("cat /proc/uptime")
            uptime_seconds = float(uptime_raw.split()[0])
            hours = int(uptime_seconds // 3600)
            minutes = int((uptime_seconds % 3600) // 60)
            info["uptime"] = f"{hours}h {minutes}m"
        except Exception as e:
            logger.debug(f"Error obteniendo uptime: {e}")
            info["uptime"] = "N/A"
        
        return info
    
    def print_info(self) -> None:
        """Imprime la información del dispositivo en formato legible."""
        info = self.safe_execute()
        if not info:
            return
        
        print("\n=== Información del Dispositivo ===")
        print(f"Serial:          {info.get('serial', 'N/A')}")
        print(f"Marca:           {info.get('brand', 'N/A')}")
        print(f"Fabricante:      {info.get('manufacturer', 'N/A')}")
        print(f"Modelo:          {info.get('model', 'N/A')}")
        print(f"Android:         {info.get('android_version', 'N/A')}")
        print(f"SDK:             {info.get('sdk_version', 'N/A')}")
        print(f"Build ID:        {info.get('build_id', 'N/A')}")
        print(f"Tipo Build:      {info.get('build_type', 'N/A')}")
        print(f"Parche Seguro:   {info.get('security_patch', 'N/A')}")
        print(f"CPU ABI:         {info.get('cpu_abi', 'N/A')}")
        print(f"Hardware:        {info.get('hardware', 'N/A')}")
        print(f"Resolución:      {info.get('resolution', 'N/A')}")
        print(f"Densidad:        {info.get('density', 'N/A')}")
        print(f"Uptime:          {info.get('uptime', 'N/A')}")
        print()