"""
Gestión de multimedia (fotos, videos, audio).
"""

from typing import Any, Dict, List, Optional

from core.adb_wrapper import ADBWrapper
from core.logger import logger
from core.modules.base import BaseModule
from core.modules.registry import registry


@registry.register
class MediaModule(BaseModule):
    """Archivos multimedia."""
    
    name = "media"
    description = "Gestión de multimedia"
    requires_device = True
    requires_root = False
    danger_level = "low"
    
    def __init__(self, adb: Optional[ADBWrapper] = None) -> None:
        super().__init__(adb)
    
    def list_images(self, limit: int = 50) -> List[str]:
        """Lista imágenes recientes."""
        self.require_device()
        
        try:
            output = self.adb.shell(
                f"find /sdcard/DCIM /sdcard/Pictures -type f -name '*.jpg' -o -name '*.png' 2>/dev/null | head -n {limit}"
            )
            return [line.strip() for line in output.strip().split('\n') if line.strip()]
        except Exception as e:
            logger.error(f"Error: {e}")
            return []
    
    def list_videos(self, limit: int = 50) -> List[str]:
        """Lista videos recientes."""
        self.require_device()
        
        try:
            output = self.adb.shell(
                f"find /sdcard/DCIM /sdcard/Movies -type f -name '*.mp4' -o -name '*.mkv' 2>/dev/null | head -n {limit}"
            )
            return [line.strip() for line in output.strip().split('\n') if line.strip()]
        except Exception as e:
            logger.error(f"Error: {e}")
            return []
    
    def list_audio(self, limit: int = 50) -> List[str]:
        """Lista archivos de audio."""
        self.require_device()
        
        try:
            output = self.adb.shell(
                f"find /sdcard/Music -type f -name '*.mp3' -o -name '*.ogg' -o -name '*.wav' 2>/dev/null | head -n {limit}"
            )
            return [line.strip() for line in output.strip().split('\n') if line.strip()]
        except Exception as e:
            logger.error(f"Error: {e}")
            return []
    
    def execute(self, action: str = "images", **kwargs) -> Any:
        actions = {
            "images": lambda: self.list_images(kwargs.get("limit", 50)),
            "videos": lambda: self.list_videos(kwargs.get("limit", 50)),
            "audio": lambda: self.list_audio(kwargs.get("limit", 50)),
        }
        
        if action not in actions:
            from core.errors import ADBError
            raise ADBError(f"Acción desconocida: {action}")
        
        return actions[action]()