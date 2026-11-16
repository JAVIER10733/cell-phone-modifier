"""
Módulo de información de batería.
"""

from typing import Any, Dict, Optional

from core.adb_wrapper import ADBWrapper
from core.logger import logger
from core.modules.base import BaseModule
from core.modules.registry import registry


@registry.register
class BatteryModule(BaseModule):
    """Obtiene información de la batería."""
    
    name = "battery"
    description = "Información de la batería"
    requires_device = True
    requires_root = False
    danger_level = "low"
    
    def __init__(self, adb: Optional[ADBWrapper] = None) -> None:
        super().__init__(adb)
    
    def execute(self, **kwargs) -> Dict[str, Any]:
        """
        Obtiene información de la batería.
        
        Returns:
            Dict[str, Any]: Información de la batería
        """
        self.require_device()
        
        try:
            output = self.adb.shell("dumpsys battery")
        except Exception as e:
            logger.error(f"Error obteniendo info de batería: {e}")
            return {"error": str(e)}
        
        info: Dict[str, Any] = {}
        
        for line in output.split('\n'):
            line = line.strip()
            if ':' not in line:
                continue
            
            key, value = line.split(':', 1)
            key = key.strip().lower().replace(' ', '_')
            value = value.strip()
            
            # Convertir valores numéricos
            try:
                if '.' in value:
                    info[key] = float(value)
                else:
                    info[key] = int(value)
            except ValueError:
                info[key] = value
        
        # Interpretar estado
        status_map = {
            1: "Desconocido",
            2: "Cargando",
            3: "Descargando",
            4: "No cargando",
            5: "Completo",
        }
        
        if "status" in info:
            info["status_text"] = status_map.get(info["status"], "Desconocido")
        
        # Interpretar fuente de alimentación
        plugged_map = {
            0: "Ninguna",
            1: "AC",
            2: "USB",
            4: "Inalámbrica",
        }
        
        if "plugged" in info:
            info["plugged_text"] = plugged_map.get(info["plugged"], "Desconocido")
        
        # Interpretar salud
        health_map = {
            1: "Desconocido",
            2: "Bueno",
            3: "Sobrecalentamiento",
            4: "Muerto",
            5: "Sobrevoltaje",
            6: "Fallo",
            7: "Frío",
        }
        
        if "health" in info:
            info["health_text"] = health_map.get(info["health"], "Desconocido")
        
        return info
    
    def print_info(self) -> None:
        """Imprime la información de batería."""
        info = self.safe_execute()
        if not info or "error" in info:
            print(f"❌ Error: {info.get('error', 'Desconocido')}")
            return
        
        print("\n=== Información de Batería ===")
        print(f"Nivel:           {info.get('level', 'N/A')}%")
        print(f"Escala:          {info.get('scale', 'N/A')}")
        print(f"Estado:          {info.get('status_text', 'N/A')}")
        print(f"Salud:           {info.get('health_text', 'N/A')}")
        print(f"Fuente:          {info.get('plugged_text', 'N/A')}")
        print(f"Tecnología:      {info.get('technology', 'N/A')}")
        print(f"Voltaje:         {info.get('voltage', 'N/A')} mV")
        print(f"Temperatura:     {info.get('temperature', 'N/A')} °C (x10)")
        print()