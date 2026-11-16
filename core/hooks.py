"""
Sistema de hooks para ejecutar código antes y después de operaciones.
"""

from typing import Any, Callable, Dict, List, Optional


class HookManager:
    """Gestiona hooks antes y después de operaciones."""
    
    def __init__(self) -> None:
        self._before_hooks: Dict[str, List[Callable]] = {}
        self._after_hooks: Dict[str, List[Callable]] = {}
    
    def register_before(self, event: str, callback: Callable) -> None:
        """
        Registra un hook que se ejecuta antes de un evento.
        
        Args:
            event: Nombre del evento
            callback: Función a ejecutar
        """
        if event not in self._before_hooks:
            self._before_hooks[event] = []
        self._before_hooks[event].append(callback)
    
    def register_after(self, event: str, callback: Callable) -> None:
        """
        Registra un hook que se ejecuta después de un evento.
        
        Args:
            event: Nombre del evento
            callback: Función a ejecutar
        """
        if event not in self._after_hooks:
            self._after_hooks[event] = []
        self._after_hooks[event].append(callback)
    
    def run_before(self, event: str, data: Any = None) -> None:
        """Ejecuta todos los hooks before de un evento."""
        if event not in self._before_hooks:
            return
        
        for callback in self._before_hooks[event]:
            try:
                callback(data)
            except Exception as e:
                from core.logger import logger
                logger.error(f"Error en hook before {event}: {e}")
    
    def run_after(self, event: str, data: Any = None) -> None:
        """Ejecuta todos los hooks after de un evento."""
        if event not in self._after_hooks:
            return
        
        for callback in self._after_hooks[event]:
            try:
                callback(data)
            except Exception as e:
                from core.logger import logger
                logger.error(f"Error en hook after {event}: {e}")
    
    def clear(self, event: Optional[str] = None) -> None:
        """
        Limpia hooks.
        
        Args:
            event: Si se especifica, limpia solo ese evento. Si no, limpia todos.
        """
        if event:
            self._before_hooks.pop(event, None)
            self._after_hooks.pop(event, None)
        else:
            self._before_hooks.clear()
            self._after_hooks.clear()