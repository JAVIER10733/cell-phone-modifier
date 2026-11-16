"""
Módulo de gestión de archivos.
"""

from pathlib import Path
from typing import Any, Dict, List, Optional

from core.adb_wrapper import ADBWrapper
from core.errors import ADBError, StorageError
from core.logger import logger
from core.modules.base import BaseModule
from core.modules.registry import registry
from core.platform_utils import check_storage_access


@registry.register
class FilesModule(BaseModule):
    """Gestiona archivos en el dispositivo."""
    
    name = "files"
    description = "Gestión de archivos"
    requires_device = True
    requires_root = False
    danger_level = "medium"
    
    def __init__(self, adb: Optional[ADBWrapper] = None) -> None:
        super().__init__(adb)
    
    def list_dir(self, remote_path: str) -> List[Dict[str, str]]:
        """
        Lista contenido de un directorio en el dispositivo.
        
        Args:
            remote_path: Ruta en el dispositivo
        
        Returns:
            List[Dict[str, str]]: Lista de archivos/directorios
        """
        self.require_device()
        
        if not remote_path:
            raise ADBError("Ruta remota requerida")
        
        try:
            output = self.adb.shell(f"ls -la {remote_path}")
        except Exception as e:
            logger.error(f"Error listando {remote_path}: {e}")
            raise ADBError(f"Error listando directorio: {e}")
        
        items = []
        for line in output.strip().split('\n'):
            if not line or line.startswith("total"):
                continue
            
            parts = line.split()
            if len(parts) < 8:
                continue
            
            permissions = parts[0]
            is_dir = permissions.startswith("d")
            name = parts[-1]
            size = parts[4]
            
            # Manejar enlaces
            if "->" in line:
                name = parts[-3]
            
            items.append({
                "name": name,
                "permissions": permissions,
                "size": size,
                "type": "dir" if is_dir else "file",
            })
        
        return items
    
    def pull_file(self, remote_path: str, local_path: str) -> bool:
        """
        Copia un archivo del dispositivo al PC.
        
        Args:
            remote_path: Ruta en el dispositivo
            local_path: Ruta local de destino
        
        Returns:
            bool: True si fue exitoso
        """
        self.require_device()
        
        if not remote_path or not local_path:
            raise ADBError("Rutas remota y local requeridas")
        
        # Verificar almacenamiento local
        local_path_obj = Path(local_path).expanduser()
        local_path_obj.parent.mkdir(parents=True, exist_ok=True)
        
        logger.info(f"Pull: {remote_path} -> {local_path}")
        return self.adb.pull(remote_path, str(local_path_obj))
    
    def push_file(self, local_path: str, remote_path: str) -> bool:
        """
        Copia un archivo del PC al dispositivo.
        
        Args:
            local_path: Ruta local del archivo
            remote_path: Ruta de destino en el dispositivo
        
        Returns:
            bool: True si fue exitoso
        """
        self.require_device()
        
        if not local_path or not remote_path:
            raise ADBError("Rutas local y remota requeridas")
        
        local_path_obj = Path(local_path).expanduser()
        if not local_path_obj.exists():
            raise StorageError(f"Archivo local no existe: {local_path}")
        
        logger.info(f"Push: {local_path} -> {remote_path}")
        return self.adb.push(str(local_path_obj), remote_path)
    
    def delete_file(self, remote_path: str) -> bool:
        """
        Elimina un archivo en el dispositivo.
        
        Args:
            remote_path: Ruta en el dispositivo
        
        Returns:
            bool: True si fue exitoso
        """
        self.require_device()
        
        if not remote_path:
            raise ADBError("Ruta remota requerida")
        
        try:
            self.adb.shell(f"rm -f {remote_path}")
            return True
        except Exception as e:
            logger.error(f"Error eliminando {remote_path}: {e}")
            return False
    
    def execute(self, action: str = "list", **kwargs) -> Any:
        """Ejecuta una acción sobre archivos."""
        if action == "list":
            return self.list_dir(kwargs.get("path", "/sdcard"))
        
        elif action == "pull":
            return self.pull_file(
                kwargs.get("remote_path"),
                kwargs.get("local_path")
            )
        
        elif action == "push":
            return self.push_file(
                kwargs.get("local_path"),
                kwargs.get("remote_path")
            )
        
        elif action == "delete":
            return self.delete_file(kwargs.get("path"))
        
        else:
            raise ADBError(f"Acción desconocida: {action}")
    
    def print_list(self, path: str = "/sdcard") -> None:
        """Imprime el contenido de un directorio."""
        items = self.list_dir(path)
        
        print(f"\n=== Contenido de {path} ({len(items)} items) ===")
        for item in items:
            icon = "📁" if item["type"] == "dir" else "📄"
            print(f"{icon} {item['name']:<40} {item['size']:>10} {item['permissions']}")
        print()