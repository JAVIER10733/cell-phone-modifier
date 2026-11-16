"""
Módulo de información de almacenamiento.
"""

from typing import Any, Dict, List, Optional

from core.adb_wrapper import ADBWrapper
from core.logger import logger
from core.modules.base import BaseModule
from core.modules.registry import registry


@registry.register
class StorageModule(BaseModule):
    """Obtiene información del almacenamiento."""
    
    name = "storage"
    description = "Información del almacenamiento"
    requires_device = True
    requires_root = False
    danger_level = "low"
    
    def __init__(self, adb: Optional[ADBWrapper] = None) -> None:
        super().__init__(adb)
    
    def _parse_df_output(self, output: str) -> List[Dict[str, Any]]:
        """Parsea la salida del comando df."""
        partitions = []
        lines = output.strip().split('\n')
        
        if len(lines) < 2:
            return partitions
        
        # Saltar encabezado
        for line in lines[1:]:
            parts = line.split()
            if len(parts) < 6:
                continue
            
            try:
                partition = {
                    "filesystem": parts[0],
                    "size_kb": int(parts[1]),
                    "used_kb": int(parts[2]),
                    "available_kb": int(parts[3]),
                    "use_percent": parts[4],
                    "mount_point": parts[5],
                }
                
                # Convertir a MB/GB
                partition["size_mb"] = partition["size_kb"] / 1024
                partition["used_mb"] = partition["used_kb"] / 1024
                partition["available_mb"] = partition["available_kb"] / 1024
                
                if partition["size_mb"] > 1024:
                    partition["size_gb"] = partition["size_mb"] / 1024
                    partition["used_gb"] = partition["used_mb"] / 1024
                    partition["available_gb"] = partition["available_mb"] / 1024
                
                partitions.append(partition)
            except (ValueError, IndexError) as e:
                logger.debug(f"Error parseando línea df: {e}")
                continue
        
        return partitions
    
    def execute(self, **kwargs) -> Dict[str, Any]:
        """
        Obtiene información del almacenamiento.
        
        Returns:
            Dict[str, Any]: Información del almacenamiento
        """
        self.require_device()
        
        try:
            output = self.adb.shell("df")
            partitions = self._parse_df_output(output)
        except Exception as e:
            logger.error(f"Error obteniendo info de almacenamiento: {e}")
            return {"error": str(e), "partitions": []}
        
        # Buscar particiones importantes
        data_partition = None
        system_partition = None
        cache_partition = None
        
        for p in partitions:
            mount = p["mount_point"]
            if mount == "/data":
                data_partition = p
            elif mount == "/system":
                system_partition = p
            elif mount == "/cache":
                cache_partition = p
        
        return {
            "partitions": partitions,
            "data": data_partition,
            "system": system_partition,
            "cache": cache_partition,
        }
    
    def print_info(self) -> None:
        """Imprime la información de almacenamiento."""
        info = self.safe_execute()
        if not info or "error" in info:
            print(f"❌ Error: {info.get('error', 'Desconocido')}")
            return
        
        print("\n=== Información de Almacenamiento ===")
        
        if info.get("data"):
            d = info["data"]
            print(f"\n📱 Datos (/data):")
            if "size_gb" in d:
                print(f"   Total:     {d['size_gb']:.2f} GB")
                print(f"   Usado:     {d['used_gb']:.2f} GB")
                print(f"   Libre:     {d['available_gb']:.2f} GB")
            else:
                print(f"   Total:     {d['size_mb']:.2f} MB")
                print(f"   Usado:     {d['used_mb']:.2f} MB")
                print(f"   Libre:     {d['available_mb']:.2f} MB")
            print(f"   Uso:       {d['use_percent']}")
        
        if info.get("system"):
            s = info["system"]
            print(f"\n⚙️  Sistema (/system):")
            if "size_gb" in s:
                print(f"   Total:     {s['size_gb']:.2f} GB")
                print(f"   Usado:     {s['used_gb']:.2f} GB")
            else:
                print(f"   Total:     {s['size_mb']:.2f} MB")
                print(f"   Usado:     {s['used_mb']:.2f} MB")
            print(f"   Uso:       {s['use_percent']}")
        
        if info.get("cache"):
            c = info["cache"]
            print(f"\n🗂️  Cache (/cache):")
            if "size_mb" in c:
                print(f"   Total:     {c['size_mb']:.2f} MB")
                print(f"   Usado:     {c['used_mb']:.2f} MB")
            print(f"   Uso:       {c['use_percent']}")
        
        print()