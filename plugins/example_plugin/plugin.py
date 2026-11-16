"""
Plugin de ejemplo: muestra información personalizada del dispositivo.
"""

from typing import Any, Dict, Optional

from core.adb_wrapper import ADBWrapper
from core.logger import logger
from core.modules.base import BaseModule


class ExamplePlugin(BaseModule):
    """
    Plugin de ejemplo que obtiene información personalizada.
    
    Este plugin demuestra:
    - Cómo heredar de BaseModule
    - Cómo registrarse automáticamente
    - Cómo ejecutar comandos ADB personalizados
    """
    
    name = "example_plugin"
    description = "Plugin de ejemplo - información personalizada"
    requires_device = True
    requires_root = False
    danger_level = "low"
    
    def __init__(self, adb: Optional[ADBWrapper] = None) -> None:
        super().__init__(adb)
    
    def get_custom_info(self) -> Dict[str, Any]:
        """
        Obtiene información personalizada del dispositivo.
        
        Returns:
            Dict[str, Any]: Información personalizada
        """
        self.require_device()
        
        info: Dict[str, Any] = {}
        
        # Obtener propiedades personalizadas
        custom_props = [
            "ro.product.locale",
            "ro.build.display.id",
            "ro.build.tags",
            "ro.build.fingerprint",
            "gsm.sim.operator.alpha",
            "gsm.sim.operator.numeric",
            "gsm.network.type",
        ]
        
        for prop in custom_props:
            try:
                value = self.adb.get_property(prop)
                info[prop] = value if value else "N/A"
            except Exception as e:
                logger.debug(f"Error obteniendo {prop}: {e}")
                info[prop] = "Error"
        
        # Obtener información adicional
        try:
            info["screen_on"] = self.adb.shell("dumpsys power | grep 'Display Power'")
        except Exception:
            info["screen_on"] = "N/A"
        
        try:
            info["cpu_temp"] = self.adb.shell("cat /sys/class/thermal/thermal_zone0/temp")
        except Exception:
            info["cpu_temp"] = "N/A"
        
        return info
    
    def execute(self, **kwargs) -> Any:
        return self.get_custom_info()
    
    def print_info(self) -> None:
        """Imprime la información personalizada."""
        info = self.safe_execute()
        if not info:
            return
        
        print("\n=== Información Personalizada (Plugin Ejemplo) ===")
        for key, value in info.items():
            print(f"  {key}: {value}")
        print()


# Auto-registro al importar
from core.modules.registry import registry

if "example_plugin" not in [m["name"] for m in registry.list_modules()]:
    registry.register(ExamplePlugin)