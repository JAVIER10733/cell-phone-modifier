"""
Notificaciones con termux-api.
"""

from typing import Any, Optional

from core.errors import TermuxError
from core.logger import logger
from core.modules.base import BaseModule
from core.modules.registry import registry
from core.termux_api import termux_api


@registry.register
class NotificationsModule(BaseModule):
    """Notificaciones del sistema."""
    
    name = "notifications"
    description = "Notificaciones con termux-api"
    requires_device = False
    requires_root = False
    danger_level = "low"
    
    def __init__(self) -> None:
        super().__init__()
    
    def send(self, title: str, content: str, priority: str = "default") -> bool:
        """Envía una notificación."""
        if not termux_api.available:
            raise TermuxError("termux-api no está instalado")
        
        return termux_api.send_notification(title, content, priority)
    
    def toast(self, message: str) -> bool:
        """Muestra un toast."""
        if not termux_api.available:
            raise TermuxError("termux-api no está instalado")
        
        return termux_api.toast(message)
    
    def execute(self, action: str = "send", **kwargs) -> Any:
        if action == "send":
            return self.send(
                kwargs.get("title", ""),
                kwargs.get("content", ""),
                kwargs.get("priority", "default")
            )
        elif action == "toast":
            return self.toast(kwargs.get("message", ""))
        return False