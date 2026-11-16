"""
Módulo de backup de aplicaciones y datos.
"""

from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

from core.adb_wrapper import ADBWrapper
from core.errors import ADBError, StorageError
from core.logger import logger
from core.modules.base import BaseModule
from core.modules.registry import registry
from core.platform_utils import check_storage_access, get_termux_paths


@registry.register
class BackupModule(BaseModule):
    """Backup de aplicaciones y datos."""
    
    name = "backup"
    description = "Backup de aplicaciones y datos"
    requires_device = True
    requires_root = False
    danger_level = "low"
    
    def __init__(self, adb: Optional[ADBWrapper] = None) -> None:
        super().__init__(adb)
    
    def _get_backup_dir(self) -> Path:
        """Obtiene el directorio de backups."""
        if check_storage_access():
            paths = get_termux_paths()
            backup_dir = paths["downloads"] / "cell_phone_modifier" / "backups"
        else:
            backup_dir = Path.home() / "cell_phone_modifier" / "backups"
        
        backup_dir.mkdir(parents=True, exist_ok=True)
        return backup_dir
    
    def backup_apk(self, package: str, output_dir: Optional[str] = None) -> str:
        """
        Hace backup del APK de una aplicación.
        
        Args:
            package: Nombre del paquete
            output_dir: Directorio de destino (opcional)
        
        Returns:
            str: Ruta local del APK guardado
        """
        self.require_device()
        
        if not package:
            raise ADBError("Nombre de paquete requerido")
        
        # Obtener ruta del APK
        try:
            output = self.adb.shell(f"pm path {package}")
            if not output:
                raise ADBError(f"Paquete no encontrado: {package}")
            
            # Tomar la primera ruta (APK base)
            apk_path = output.split('\n')[0].replace("package:", "").strip()
        except Exception as e:
            raise ADBError(f"Error obteniendo ruta de APK: {e}")
        
        # Determinar directorio de salida
        if output_dir:
            output_path = Path(output_dir).expanduser()
        else:
            output_path = self._get_backup_dir() / "apks"
        
        output_path.mkdir(parents=True, exist_ok=True)
        
        local_apk = output_path / f"{package}.apk"
        
        logger.info(f"Backup APK: {package} -> {local_apk}")
        
        if not self.adb.pull(apk_path, str(local_apk)):
            raise ADBError(f"Error copiando APK de {package}")
        
        return str(local_apk)
    
    def backup_all_apks(self, output_dir: Optional[str] = None) -> List[str]:
        """
        Hace backup de todos los APKs de apps de usuario.
        
        Args:
            output_dir: Directorio de destino (opcional)
        
        Returns:
            List[str]: Lista de rutas de APKs guardados
        """
        from core.modules.apps import AppsModule
        
        self.require_device()
        
        apps_module = AppsModule(self.adb)
        packages = apps_module.list_packages(include_system=False)
        
        saved = []
        total = len(packages)
        
        print(f"\n📦 Haciendo backup de {total} aplicaciones...")
        
        for i, package in enumerate(packages, 1):
            try:
                print(f"[{i}/{total}] {package}...", end=" ", flush=True)
                path = self.backup_apk(package, output_dir)
                saved.append(path)
                print("✅")
            except Exception as e:
                print(f"❌ {e}")
                logger.error(f"Error backup {package}: {e}")
        
        print(f"\n✅ {len(saved)}/{total} APKs guardados")
        return saved
    
    def adb_backup(self, output_file: Optional[str] = None, include_apks: bool = True) -> str:
        """
        Hace backup completo usando adb backup.
        
        Args:
            output_file: Archivo de destino
            include_apks: Incluir APKs en el backup
        
        Returns:
            str: Ruta del archivo de backup
        """
        self.require_device()
        
        if output_file:
            output_path = Path(output_file).expanduser()
        else:
            backup_dir = self._get_backup_dir()
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_path = backup_dir / f"full_backup_{timestamp}.ab"
        
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        args = ["backup"]
        if include_apks:
            args.append("-apk")
        args.extend(["-f", str(output_path), "-all"])
        
        logger.info(f"Backup completo: {output_path}")
        print("\n⚠️  El dispositivo pedirá confirmación y contraseña para el backup.")
        print("   Esto puede tardar varios minutos...\n")
        
        result = self.adb._execute(args, check=False, timeout=3600)
        
        if result.returncode != 0:
            raise ADBError(f"Backup falló: {result.stderr}")
        
        return str(output_path)
    
    def execute(self, action: str = "apk", **kwargs) -> Any:
        """Ejecuta una acción de backup."""
        if action == "apk":
            return self.backup_apk(
                kwargs.get("package"),
                kwargs.get("output_dir")
            )
        
        elif action == "all_apks":
            return self.backup_all_apks(kwargs.get("output_dir"))
        
        elif action == "full":
            return self.adb_backup(
                kwargs.get("output_file"),
                kwargs.get("include_apks", True)
            )
        
        else:
            raise ADBError(f"Acción desconocida: {action}")