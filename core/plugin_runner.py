"""
Ejecutor de plugins y módulos externos.
"""

import importlib
import importlib.util
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Type

from core.errors import CellPhoneModifierError
from core.logger import logger
from core.modules.base import BaseModule


class PluginRunner:
    """Ejecuta plugins y módulos externos."""
    
    def __init__(self, plugins_dir: Optional[Path] = None) -> None:
        if plugins_dir:
            self.plugins_dir = plugins_dir
        else:
            self.plugins_dir = Path(__file__).parent.parent / "plugins"
        
        self.plugins_dir.mkdir(parents=True, exist_ok=True)
        self._loaded_plugins: Dict[str, Any] = {}
    
    def discover_plugins(self) -> List[Dict[str, str]]:
        """
        Descubre plugins disponibles.
        
        Returns:
            List[Dict[str, str]]: Lista de plugins encontrados
        """
        plugins = []
        
        if not self.plugins_dir.exists():
            return plugins
        
        for item in self.plugins_dir.iterdir():
            if item.is_dir() and (item / "__init__.py").exists():
                plugin_info = {
                    "name": item.name,
                    "path": str(item),
                    "status": "available"
                }
                
                if item.name in self._loaded_plugins:
                    plugin_info["status"] = "loaded"
                
                plugins.append(plugin_info)
        
        return plugins
    
    def load_plugin(self, plugin_name: str) -> Optional[Type[BaseModule]]:
        """
        Carga un plugin por nombre.
        
        Args:
            plugin_name: Nombre del plugin
        
        Returns:
            Optional[Type[BaseModule]]: Clase del módulo del plugin
        """
        plugin_dir = self.plugins_dir / plugin_name
        
        if not plugin_dir.exists():
            logger.error(f"Plugin no encontrado: {plugin_name}")
            return None
        
        init_file = plugin_dir / "__init__.py"
        if not init_file.exists():
            logger.error(f"Plugin {plugin_name} no tiene __init__.py")
            return None
        
        try:
            spec = importlib.util.spec_from_file_location(
                f"plugins.{plugin_name}",
                str(init_file)
            )
            
            if not spec or not spec.loader:
                logger.error(f"No se pudo cargar spec de {plugin_name}")
                return None
            
            module = importlib.util.module_from_spec(spec)
            sys.modules[f"plugins.{plugin_name}"] = module
            spec.loader.exec_module(module)
            
            # Buscar clase que herede de BaseModule
            for attr_name in dir(module):
                attr = getattr(module, attr_name)
                if (
                    isinstance(attr, type)
                    and issubclass(attr, BaseModule)
                    and attr is not BaseModule
                ):
                    self._loaded_plugins[plugin_name] = attr
                    logger.info(f"Plugin cargado: {plugin_name} -> {attr_name}")
                    return attr
            
            logger.warning(f"Plugin {plugin_name} no tiene módulos válidos")
            return None
        
        except Exception as e:
            logger.error(f"Error cargando plugin {plugin_name}: {e}")
            return None
    
    def run_plugin(self, plugin_name: str, **kwargs) -> Any:
        """
        Ejecuta un plugin.
        
        Args:
            plugin_name: Nombre del plugin
            **kwargs: Argumentos del plugin
        
        Returns:
            Any: Resultado del plugin
        """
        if plugin_name not in self._loaded_plugins:
            module_class = self.load_plugin(plugin_name)
            if not module_class:
                raise CellPhoneModifierError(f"Plugin no disponible: {plugin_name}")
        else:
            module_class = self._loaded_plugins[plugin_name]
        
        module = module_class()
        return module.safe_execute(**kwargs)
    
    def unload_plugin(self, plugin_name: str) -> None:
        """Descarga un plugin."""
        if plugin_name in self._loaded_plugins:
            del self._loaded_plugins[plugin_name]
            logger.info(f"Plugin descargado: {plugin_name}")
    
    def get_loaded_plugins(self) -> List[str]:
        """Lista plugins cargados."""
        return list(self._loaded_plugins.keys())