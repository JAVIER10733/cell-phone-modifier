"""
Módulo de logs del sistema (logcat, dmesg).
"""

from datetime import datetime
from pathlib import Path
from typing import Any, Optional

from core.adb_wrapper import ADBWrapper
from core.errors import ADBError
from core.logger import logger
from core.modules.base import BaseModule
from core.modules.registry import registry
from core.platform_utils import check_storage_access, get_termux_paths


@registry.register
class LogsModule(BaseModule):
    """Logs del sistema Android."""
    
    name = "logs"
    description = "Logs del sistema (logcat, dmesg)"
    requires_device = True
    requires_root = False
    danger_level = "low"
    
    def __init__(self, adb: Optional[ADBWrapper] = None) -> None:
        super().__init__(adb)
    
    def _get_logs_dir(self) -> Path:
        """Obtiene el directorio para guardar logs."""
        if check_storage_access():
            paths = get_termux_paths()
            logs_dir = paths["downloads"] / "cell_phone_modifier" / "logs"
        else:
            logs_dir = Path.home() / "cell_phone_modifier" / "logs"
        
        logs_dir.mkdir(parents=True, exist_ok=True)
        return logs_dir
    
    def get_logcat(
        self,
        lines: int = 100,
        tag: Optional[str] = None,
        priority: Optional[str] = None
    ) -> str:
        """
        Obtiene logcat del dispositivo.
        
        Args:
            lines: Número de líneas a obtener
            tag: Filtrar por tag
            priority: Filtrar por prioridad (V, D, I, W, E, F)
        
        Returns:
            str: Salida de logcat
        """
        self.require_device()
        
        args = ["logcat", "-d", "-t", str(lines)]
        
        if tag:
            args.extend(["-s", f"{tag}:*"])
        
        if priority:
            args.append(f"*:{priority}")
        
        result = self.adb._execute(args, check=False)
        return result.stdout
    
    def get_dmesg(self, lines: int = 100) -> str:
        """
        Obtiene dmesg del dispositivo (puede requerir root).
        
        Args:
            lines: Número de líneas a obtener
        
        Returns:
            str: Salida de dmesg
        """
        self.require_device()
        
        try:
            output = self.adb.shell(f"dmesg | tail -n {lines}")
            return output
        except Exception as e:
            logger.warning(f"dmesg puede requerir root: {e}")
            raise ADBError(f"Error obteniendo dmesg (¿requiere root?): {e}")
    
    def save_logcat(self, output_file: Optional[str] = None, lines: int = 1000) -> str:
        """
        Guarda logcat en un archivo.
        
        Args:
            output_file: Ruta del archivo de destino
            lines: Número de líneas
        
        Returns:
            str: Ruta del archivo guardado
        """
        self.require_device()
        
        if output_file:
            output_path = Path(output_file).expanduser()
        else:
            logs_dir = self._get_logs_dir()
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_path = logs_dir / f"logcat_{timestamp}.txt"
        
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        logcat_output = self.get_logcat(lines=lines)
        
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(logcat_output)
        
        logger.info(f"Logcat guardado en: {output_path}")
        return str(output_path)
    
    def clear_logcat(self) -> bool:
        """
        Limpia el buffer de logcat.
        
        Returns:
            bool: True si fue exitoso
        """
        self.require_device()
        
        try:
            self.adb.shell("logcat -c")
            logger.info("Logcat limpiado")
            return True
        except Exception as e:
            logger.error(f"Error limpiando logcat: {e}")
            return False
    
    def execute(self, action: str = "logcat", **kwargs) -> Any:
        """Ejecuta una acción sobre logs."""
        if action == "logcat":
            return self.get_logcat(
                lines=kwargs.get("lines", 100),
                tag=kwargs.get("tag"),
                priority=kwargs.get("priority")
            )
        
        elif action == "logcat_save":
            return self.save_logcat(
                kwargs.get("output_file"),
                kwargs.get("lines", 1000)
            )
        
        elif action == "dmesg":
            return self.get_dmesg(kwargs.get("lines", 100))
        
        elif action == "clear":
            return self.clear_logcat()
        
        else:
            raise ADBError(f"Acción desconocida: {action}")
    
    def print_logcat(self, lines: int = 50) -> None:
        """Imprime las últimas líneas de logcat."""
        output = self.get_logcat(lines=lines)
        print(f"\n=== Logcat (últimas {lines} líneas) ===")
        print(output)