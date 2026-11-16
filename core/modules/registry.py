"""
Registro central de módulos disponibles.
Permite registrar módulos mediante decoradores y consultarlos por nombre.
"""

from typing import Dict, List, Optional, Type

from core.errors import CellPhoneModifierError
from core.logger import logger
from core.modules.base import BaseModule


class ModuleRegistry:
    """Registro central de módulos."""
    
    def __init__(self) -> None:
        self._modules: Dict[str, Type[BaseModule]] = {}
    
    def register(self, module_class: Type[BaseModule]) -> Type[BaseModule]:
        """
        Registra un módulo. Se usa como decorador.
        
        Args:
            module_class: Clase del módulo a registrar
        
        Returns:
            Type[BaseModule]: La misma clase (para usar como decorador)
        
        Raises:
            CellPhoneModifierError: Si la clase no hereda de BaseModule
        """
        if not issubclass(module_class, BaseModule):
            raise CellPhoneModifierError(
                f"{module_class.__name__} no es subclase de BaseModule"
            )
        
        name = module_class.name
        if name in self._modules:
            logger.warning(f"Módulo '{name}' ya registrado, sobrescribiendo")
        
        self._modules[name] = module_class
        logger.debug(f"Módulo registrado: {name}")
        return module_class
    
    def get(self, name: str) -> Optional[Type[BaseModule]]:
        """
        Obtiene un módulo por nombre.
        
        Args:
            name: Nombre del módulo
        
        Returns:
            Optional[Type[BaseModule]]: Clase del módulo o None si no existe
        """
        return self._modules.get(name)
    
    def list_modules(self) -> List[Dict[str, str]]:
        """
        Lista todos los módulos registrados con su metadata.
        
        Returns:
            List[Dict[str, str]]: Lista de diccionarios con info de los módulos
        """
        modules = []
        for name, module_class in self._modules.items():
            modules.append({
                "name": name,
                "description": module_class.description,
                "requires_device": str(module_class.requires_device),
                "requires_root": str(module_class.requires_root),
                "danger_level": module_class.danger_level,
            })
        return modules
    
    def print_modules(self) -> None:
        """Imprime la lista de módulos en formato legible para la consola."""
        modules = self.list_modules()
        
        if not modules:
            print("No hay módulos registrados.")
            return
        
        print("\n=== Módulos Disponibles ===")
        print(f"{'Nombre':<20} {'Descripción':<40} {'Dispositivo':<12} {'Root':<6} {'Peligro':<10}")
        print("-" * 88)
        
        for mod in modules:
            device_icon = "✅" if mod["requires_device"] == "True" else "❌"
            root_icon = "✅" if mod["requires_root"] == "True" else "❌"
            print(
                f"{mod['name']:<20} {mod['description']:<40} "
                f"{device_icon:<12} {root_icon:<6} {mod['danger_level']:<10}"
            )
        print()


# Instancia global del registro
registry = ModuleRegistry()