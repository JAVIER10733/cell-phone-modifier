"""
Módulo de restauración de backups.
"""

from pathlib import Path
from typing import Any, Optional

from core.adb_wrapper import ADBWrapper
from core.errors import ADBError, StorageError
from core.logger import logger
from core.modules.base import BaseModule
from core.modules.registry import registry


@registry.register
class RestoreModule(BaseModule):
    """Restauración de backups."""
    
    name = "restore"
    description = "Restauración de backups"
    requires_device = True
    requires_root = False
    danger_level = "high"  # Restaurar puede sobreescribir datos
    
    def __init__(self, adb: Optional[ADBWrapper] = None) -> None:
        super().__init__(adb)
    
    def restore_apk(self, apk_path: str, replace: bool = True) -> bool:
        """
        Restaura una APK.
        
        Args:
            apk_path: Ruta local del APK
            replace: Si True, reemplaza si ya existe
        
        Returns:
            bool: True si fue exitoso
        """
        self.require_device()
        
        apk_path_obj = Path(apk_path).expanduser()
        if not apk_path_obj.exists():
            raise StorageError(f"APK no existe: {apk_path}")
        
        logger.info(f"Restaurando APK: {apk_path}")
        return self.adb.install(str(apk_path_obj), replace=replace)
    
    def adb_restore(self, backup_file: str) -> bool:
        """
        Restaura un backup completo de adb backup.
        
        Args:
            backup_file: Ruta del archivo .ab
        
        Returns:
            bool: True si fue exitoso
        """
        self.require_device()
        
        backup_path = Path(backup_file).expanduser()
        if not backup_path.exists():
            raise StorageError(f"Archivo de backup no existe: {backup_file}")
        
        logger.info(f"Restaurando backup: {backup_file}")
        print("\n⚠️  El dispositivo pedirá confirmación y contraseña.")
        print("   Esto puede tardar varios minutos...\n")
        
        result = self.adb._execute(
            ["restore", str(backup_path)],
            check=False,
            timeout=3600
        )
        
        if result.returncode != 0:
            raise ADBError(f"Restauración falló: {result.stderr}")
        
        return True
    
    def execute(self, action: str = "apk", **kwargs) -> Any:
        """Ejecuta una acción de restauración."""
        if action == "apk":
            return self.restore_apk(
                kwargs.get("apk_path"),
                kwargs.get("replace", True)
            )
        
        elif action == "full":
            return self.adb_restore(kwargs.get("backup_file"))
        
        else:
            raise ADBError(f"Acción desconocida: {action}")