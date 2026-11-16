"""
Bus de eventos interno para cell_phone_modifier.
Permite comunicación desacoplada entre módulos.
"""

from typing import Any, Callable, Dict, List, Optional

from core.logger import logger


class EventBus:
    """Bus de eventos simple y síncrono."""
    
    def __init__(self) -> None:
        self._listeners: Dict[str, List[Callable]] = {}
    
    def on(self, event: str, callback: Callable) -> None:
        """
        Registra un listener para un evento.
        
        Args:
            event: Nombre del evento
            callback: Función a llamar cuando ocurra el evento
        """
        if event not in self._listeners:
            self._listeners[event] = []
        
        if callback not in self._listeners[event]:
            self._listeners[event].append(callback)
    
    def off(self, event: str, callback: Optional[Callable] = None) -> None:
        """
        Elimina un listener.
        
        Args:
            event: Nombre del evento
            callback: Listener a eliminar. Si es None, elimina todos los de ese evento.
        """
        if event not in self._listeners:
            return
        
        if callback is None:
            del self._listeners[event]
        else:
            self._listeners[event] = [
                cb for cb in self._listeners[event] if cb != callback
            ]
    
    def emit(self, event: str, data: Any = None) -> None:
        """
        Emite un evento y llama a todos los listeners registrados.
        
        Args:
            event: Nombre del evento
            data: Datos a pasar a los listeners
        """
        if event not in self._listeners:
            return
        
        # Copiar la lista para evitar problemas si un listener se desregistra durante la ejecución
        listeners = self._listeners[event].copy()
        
        for callback in listeners:
            try:
                callback(data)
            except Exception as e:
                logger.error(f"Error en listener de evento '{event}': {e}")
    
    def once(self, event: str, callback: Callable) -> None:
        """
        Registra un listener que se ejecuta una sola vez y luego se elimina.
        
        Args:
            event: Nombre del evento
            callback: Función a llamar
        """
        def wrapper(data: Any) -> None:
            callback(data)
            self.off(event, wrapper)
        
        self.on(event, wrapper)
    
    def clear(self, event: Optional[str] = None) -> None:
        """
        Limpia los listeners.
        
        Args:
            event: Si se especifica, limpia solo ese evento. Si no, limpia todos.
        """
        if event:
            self._listeners.pop(event, None)
        else:
            self._listeners.clear()
    
    def get_events(self) -> List[str]:
        """Lista todos los eventos que tienen listeners registrados."""
        return list(self._listeners.keys())
    
    def has_listeners(self, event: str) -> bool:
        """Verifica si un evento tiene listeners registrados."""
        return event in self._listeners and len(self._listeners[event]) > 0


# Instancia global para uso en toda la aplicación
event_bus = EventBus()