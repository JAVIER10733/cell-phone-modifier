"""
Módulo de capturas de pantalla y grabación.
"""

from datetime import datetime
from pathlib import Path
from typing import Any, Optional

from core.adb_wrapper import ADBWrapper
from core.errors import ADBError, StorageError
from core.logger import logger
from core.modules.base import BaseModule
from core.modules.registry import registry
from core.platform_utils import check_storage_access, get_termux_paths


@registry.register
class ScreenshotsModule(BaseModule):
    """Capturas de pantalla y grabación de video."""
    
    name = "screenshots"
    description = "Capturas y grabación de pantalla"
    requires_device = True
    requires_root = False
    danger_level = "low"
    
    REMOTE_PATH = "/sdcard/cell_phone_modifier_screenshot.png"
    REMOTE_VIDEO_PATH = "/sdcard/cell_phone_modifier_video.mp4"
    
    def __init__(self, adb: Optional[ADBWrapper] = None) -> None:
        super().__init__(adb)
    
    def _get_local_dir(self) -> Path:
        """Obtiene el directorio local para guardar capturas."""
        if check_storage_access():
            paths = get_termux_paths()
            local_dir = paths["downloads"] / "cell_phone_modifier" / "screenshots"
        else:
            local_dir = Path.home() / "cell_phone_modifier" / "screenshots"
        
        local_dir.mkdir(parents=True, exist_ok=True)
        return local_dir
    
    def take_screenshot(self, local_path: Optional[str] = None) -> str:
        """
        Toma una captura de pantalla.
        
        Args:
            local_path: Ruta local donde guardar. Si es None, usa ruta por defecto.
        
        Returns:
            str: Ruta local de la captura
        """
        self.require_device()
        
        try:
            # Tomar captura en el dispositivo
            self.adb.shell(f"screencap -p {self.REMOTE_PATH}")
            
            # Determinar ruta local
            if local_path:
                local_path_obj = Path(local_path).expanduser()
            else:
                local_dir = self._get_local_dir()
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                local_path_obj = local_dir / f"screenshot_{timestamp}.png"
            
            local_path_obj.parent.mkdir(parents=True, exist_ok=True)
            
            # Pull de la captura
            if not self.adb.pull(self.REMOTE_PATH, str(local_path_obj)):
                raise ADBError("Error al copiar captura al dispositivo local")
            
            # Limpiar archivo remoto
            try:
                self.adb.shell(f"rm -f {self.REMOTE_PATH}")
            except Exception:
                pass
            
            logger.info(f"Captura guardada en: {local_path_obj}")
            return str(local_path_obj)
        
        except Exception as e:
            logger.error(f"Error tomando captura: {e}")
            raise ADBError(f"Error tomando captura: {e}")
    
    def start_recording(self, time_limit: int = 180, bit_rate: int = 4000000) -> None:
        """
        Inicia grabación de pantalla.
        
        Args:
            time_limit: Tiempo máximo en segundos (máx 180)
            bit_rate: Bit rate en bps
        """
        self.require_device()
        
        if time_limit > 180:
            time_limit = 180
        
        # Limpiar archivo previo
        try:
            self.adb.shell(f"rm -f {self.REMOTE_VIDEO_PATH}")
        except Exception:
            pass
        
        cmd = (
            f"screenrecord "
            f"--time-limit {time_limit} "
            f"--bit-rate {bit_rate} "
            f"{self.REMOTE_VIDEO_PATH}"
        )
        
        logger.info(f"Iniciando grabación ({time_limit}s máx)...")
        print(f"🎥 Grabando pantalla (Ctrl+C para detener, máx {time_limit}s)...")
        
        # Ejecutar en background no es trivial con subprocess
        # El usuario debe detener con Ctrl+C
        try:
            self.adb.shell(cmd)
        except KeyboardInterrupt:
            print("\n⏹️  Grabación detenida")
        except Exception as e:
            logger.error(f"Error en grabación: {e}")
    
    def stop_recording_and_pull(self, local_path: Optional[str] = None) -> str:
        """
        Detiene grabación y la copia al dispositivo local.
        
        Args:
            local_path: Ruta local donde guardar
        
        Returns:
            str: Ruta local del video
        """
        self.require_device()
        
        if local_path:
            local_path_obj = Path(local_path).expanduser()
        else:
            local_dir = self._get_local_dir()
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            local_path_obj = local_dir / f"video_{timestamp}.mp4"
        
        local_path_obj.parent.mkdir(parents=True, exist_ok=True)
        
        if not self.adb.pull(self.REMOTE_VIDEO_PATH, str(local_path_obj)):
            raise ADBError("Error al copiar video al dispositivo local")
        
        # Limpiar archivo remoto
        try:
            self.adb.shell(f"rm -f {self.REMOTE_VIDEO_PATH}")
        except Exception:
            pass
        
        logger.info(f"Video guardado en: {local_path_obj}")
        return str(local_path_obj)
    
    def execute(self, action: str = "screenshot", **kwargs) -> Any:
        """Ejecuta una acción de captura."""
        if action == "screenshot":
            return self.take_screenshot(kwargs.get("local_path"))
        
        elif action == "record_start":
            return self.start_recording(
                time_limit=kwargs.get("time_limit", 180),
                bit_rate=kwargs.get("bit_rate", 4000000)
            )
        
        elif action == "record_stop":
            return self.stop_recording_and_pull(kwargs.get("local_path"))
        
        else:
            raise ADBError(f"Acción desconocida: {action}")