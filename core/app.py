"""
Orquestador principal de cell_phone_modifier.
Coordina módulos, eventos, hooks y configuración.
"""

from pathlib import Path
from typing import Any, Dict, List, Optional

from core.config import Config, config
from core.db import Database
from core.events import EventBus
from core.hooks import HookManager
from core.logger import logger, setup_logger
from core.modules.registry import registry


class App:
    """Orquestador principal de la aplicación."""
    
    def __init__(self, config_path: Optional[Path] = None) -> None:
        self.config: Config = config
        self.db: Database = Database()
        self.events: EventBus = EventBus()
        self.hooks: HookManager = HookManager()
        self.modules = registry
        self._initialized = False
        
        if config_path:
            self.config = Config(config_dir=config_path)
    
    def initialize(self) -> None:
        """Inicializa todos los subsistemas."""
        if self._initialized:
            return
        
        logger.info("Inicializando cell_phone_modifier...")
        
        # Inicializar base de datos
        self.db.initialize()
        
        # Registrar eventos del sistema
        self._register_system_events()
        
        # Cargar módulos
        self._load_modules()
        
        self._initialized = True
        logger.info("Aplicación inicializada correctamente")
    
    def _register_system_events(self) -> None:
        """Registra eventos del sistema."""
        self.events.on("app.start", lambda data: logger.info(f"App iniciada: {data}"))
        self.events.on("app.stop", lambda data: logger.info(f"App detenida: {data}"))
        self.events.on("module.execute", lambda data: logger.debug(f"Módulo ejecutado: {data}"))
        self.events.on("module.error", lambda data: logger.error(f"Error en módulo: {data}"))
    
    def _load_modules(self) -> None:
        """Carga todos los módulos registrados."""
        modules = self.modules.list_modules()
        logger.info(f"Módulos cargados: {len(modules)}")
        for mod in modules:
            logger.debug(f"  - {mod['name']}: {mod['description']}")
    
    def execute_module(self, module_name: str, **kwargs) -> Any:
        """
        Ejecuta un módulo por nombre.
        
        Args:
            module_name: Nombre del módulo
            **kwargs: Argumentos del módulo
        
        Returns:
            Any: Resultado del módulo
        """
        module_class = self.modules.get(module_name)
        if not module_class:
            raise ValueError(f"Módulo no encontrado: {module_name}")
        
        # Ejecutar hooks previos
        self.hooks.run_before(module_name, kwargs)
        
        # Emitir evento
        self.events.emit("module.execute", {"module": module_name, "args": kwargs})
        
        # Ejecutar módulo
        try:
            module = module_class()
            result = module.safe_execute(**kwargs)
            
            # Registrar en base de datos
            self.db.log_action(module_name, kwargs, result)
            
            # Emitir evento de éxito
            self.events.emit("module.success", {"module": module_name, "result": result})
            
            return result
        except Exception as e:
            self.events.emit("module.error", {"module": module_name, "error": str(e)})
            raise
        finally:
            # Ejecutar hooks posteriores
            self.hooks.run_after(module_name, kwargs)
    
    def shutdown(self) -> None:
        """Cierra la aplicación limpiamente."""
        logger.info("Cerrando aplicación...")
        self.events.emit("app.stop", {"reason": "shutdown"})
        self.db.close()
        self._initialized = False
        logger.info("Aplicación cerrada")


# Instancia global
app = App()