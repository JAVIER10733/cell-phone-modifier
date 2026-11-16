"""
Módulo de gestión de aplicaciones.
"""

from typing import Any, Dict, List, Optional

from core.adb_wrapper import ADBWrapper
from core.errors import ADBError
from core.logger import logger
from core.modules.base import BaseModule
from core.modules.registry import registry


@registry.register
class AppsModule(BaseModule):
    """Gestiona aplicaciones del dispositivo."""
    
    name = "apps"
    description = "Gestión de aplicaciones"
    requires_device = True
    requires_root = False
    danger_level = "medium"
    
    def __init__(self, adb: Optional[ADBWrapper] = None) -> None:
        super().__init__(adb)
    
    def list_packages(
        self,
        include_system: bool = False,
        include_uninstalled: bool = False
    ) -> List[str]:
        """
        Lista paquetes instalados.
        
        Args:
            include_system: Incluir apps del sistema
            include_uninstalled: Incluir apps desinstaladas pero con datos
        
        Returns:
            List[str]: Lista de nombres de paquetes
        """
        self.require_device()
        
        args = ["shell", "pm", "list", "packages"]
        
        if not include_system:
            args.append("-3")  # Solo apps de terceros
        
        if include_uninstalled:
            args.append("-u")
        
        result = self.adb._execute(args)
        
        packages = []
        for line in result.stdout.strip().split('\n'):
            if line.startswith("package:"):
                packages.append(line.replace("package:", "").strip())
        
        return sorted(packages)
    
    def get_package_info(self, package: str) -> Dict[str, Any]:
        """
        Obtiene información de un paquete.
        
        Args:
            package: Nombre del paquete
        
        Returns:
            Dict[str, Any]: Información del paquete
        """
        self.require_device()
        
        if not package or not isinstance(package, str):
            raise ADBError("Nombre de paquete inválido")
        
        try:
            output = self.adb.shell(f"dumpsys package {package}")
        except Exception as e:
            logger.error(f"Error obteniendo info de {package}: {e}")
            return {"error": str(e)}
        
        info: Dict[str, Any] = {"package": package}
        
        for line in output.split('\n'):
            line = line.strip()
            
            if "versionName=" in line:
                info["version_name"] = line.split("versionName=")[1].split()[0]
            elif "versionCode=" in line:
                info["version_code"] = line.split("versionCode=")[1].split()[0]
            elif "firstInstallTime=" in line:
                info["first_install"] = line.split("firstInstallTime=")[1].strip()
            elif "lastUpdateTime=" in line:
                info["last_update"] = line.split("lastUpdateTime=")[1].strip()
            elif "installerPackageName=" in line:
                info["installer"] = line.split("installerPackageName=")[1].strip()
        
        return info
    
    def execute(self, action: str = "list", **kwargs) -> Any:
        """
        Ejecuta una acción sobre aplicaciones.
        
        Args:
            action: Acción a ejecutar ("list", "info", "uninstall")
            **kwargs: Argumentos adicionales
        
        Returns:
            Any: Resultado de la acción
        """
        if action == "list":
            return self.list_packages(
                include_system=kwargs.get("include_system", False),
                include_uninstalled=kwargs.get("include_uninstalled", False)
            )
        
        elif action == "info":
            package = kwargs.get("package")
            if not package:
                raise ADBError("Se requiere nombre de paquete")
            return self.get_package_info(package)
        
        elif action == "uninstall":
            package = kwargs.get("package")
            if not package:
                raise ADBError("Se requiere nombre de paquete")
            keep_data = kwargs.get("keep_data", False)
            return self.adb.uninstall(package, keep_data=keep_data)
        
        elif action == "install":
            apk_path = kwargs.get("apk_path")
            if not apk_path:
                raise ADBError("Se requiere ruta de APK")
            replace = kwargs.get("replace", False)
            return self.adb.install(apk_path, replace=replace)
        
        else:
            raise ADBError(f"Acción desconocida: {action}")
    
    def print_list(self, include_system: bool = False) -> None:
        """Imprime la lista de aplicaciones."""
        packages = self.list_packages(include_system=include_system)
        
        print(f"\n=== Aplicaciones ({len(packages)}) ===")
        for i, pkg in enumerate(packages, 1):
            print(f"{i:3d}. {pkg}")
        print()