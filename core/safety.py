"""
Módulo de seguridad para cell_phone_modifier.
Maneja confirmaciones de usuario y modo dry-run.
"""

import sys
from typing import Callable, Optional

from core.errors import SafetyError
from core.logger import logger


class SafetyManager:
    """Gestiona confirmaciones y modo dry-run."""
    
    def __init__(self, dry_run: bool = False, auto_confirm: bool = False) -> None:
        """
        Inicializa el gestor de seguridad.
        
        Args:
            dry_run: Si True, no ejecuta acciones destructivas
            auto_confirm: Si True, confirma automáticamente (peligroso)
        """
        self.dry_run = dry_run
        self.auto_confirm = auto_confirm
    
    def enable_dry_run(self) -> None:
        """Activa modo dry-run."""
        self.dry_run = True
        logger.info("Modo dry-run activado")
    
    def disable_dry_run(self) -> None:
        """Desactiva modo dry-run."""
        self.dry_run = False
        logger.info("Modo dry-run desactivado")
    
    def enable_auto_confirm(self) -> None:
        """Activa auto-confirmación (peligroso)."""
        self.auto_confirm = True
        logger.warning("Auto-confirmación activada - ¡PELIGROSO!")
    
    def disable_auto_confirm(self) -> None:
        """Desactiva auto-confirmación."""
        self.auto_confirm = False
        logger.info("Auto-confirmación desactivada")
    
    def confirm(
        self,
        action: str,
        danger_level: str = "medium",
        default: bool = False
    ) -> bool:
        """
        Pide confirmación al usuario para una acción.
        
        Args:
            action: Descripción de la acción
            danger_level: Nivel de peligro ("low", "medium", "high", "critical")
            default: Valor por defecto si el usuario solo presiona Enter
        
        Returns:
            bool: True si el usuario confirma, False en caso contrario
        """
        if self.auto_confirm:
            logger.warning(f"Auto-confirmación: {action}")
            return True
        
        if self.dry_run:
            logger.info(f"[DRY-RUN] Se omitiría: {action}")
            print(f"\n⚠️  [DRY-RUN] Se omitiría: {action}")
            return False
        
        # Símbolos según nivel de peligro
        danger_symbols = {
            "low": "ℹ️",
            "medium": "⚠️",
            "high": "🔥",
            "critical": "💀"
        }
        
        symbol = danger_symbols.get(danger_level, "⚠️")
        
        default_str = "[Y/n]" if default else "[y/N]"
        prompt = f"\n{symbol} {action} {default_str}: "
        
        try:
            response = input(prompt).strip().lower()
            
            if not response:
                return default
            
            return response in ('y', 'yes', 'si', 'sí')
        
        except (EOFError, KeyboardInterrupt):
            print("\n")
            return False
    
    def confirm_critical(self, action: str) -> bool:
        """
        Pide confirmación doble para acciones críticas.
        
        Args:
            action: Descripción de la acción crítica
        
        Returns:
            bool: True si el usuario confirma dos veces
        """
        if self.auto_confirm:
            logger.warning(f"Auto-confirmación crítica: {action}")
            return True
        
        if self.dry_run:
            logger.info(f"[DRY-RUN] Se omitiría acción crítica: {action}")
            print(f"\n💀 [DRY-RUN] Se omitiría: {action}")
            return False
        
        print(f"\n💀 ACCIÓN CRÍTICA: {action}")
        print("Esta acción puede causar pérdida de datos o dañar el dispositivo.")
        
        # Primera confirmación
        if not self.confirm("¿Estás seguro de que quieres continuar?", "critical", False):
            return False
        
        # Segunda confirmación
        try:
            response = input("\n💀 Escribe 'SI' para confirmar: ").strip()
            return response == "SI"
        except (EOFError, KeyboardInterrupt):
            print("\n")
            return False
    
    def require_confirmation(
        self,
        action: str,
        danger_level: str = "medium"
    ) -> Callable:
        """
        Decorador para requerir confirmación antes de ejecutar una función.
        
        Args:
            action: Descripción de la acción
            danger_level: Nivel de peligro
        
        Returns:
            Callable: Decorador
        """
        def decorator(func: Callable) -> Callable:
            def wrapper(*args, **kwargs):
                if not self.confirm(action, danger_level):
                    logger.info(f"Acción cancelada por el usuario: {action}")
                    print(f"\n❌ Acción cancelada: {action}")
                    return None
                
                return func(*args, **kwargs)
            
            return wrapper
        
        return decorator
    
    def require_critical_confirmation(self, action: str) -> Callable:
        """
        Decorador para requerir confirmación doble para acciones críticas.
        
        Args:
            action: Descripción de la acción crítica
        
        Returns:
            Callable: Decorador
        """
        def decorator(func: Callable) -> Callable:
            def wrapper(*args, **kwargs):
                if not self.confirm_critical(action):
                    logger.info(f"Acción crítica cancelada por el usuario: {action}")
                    print(f"\n❌ Acción crítica cancelada: {action}")
                    return None
                
                return func(*args, **kwargs)
            
            return wrapper
        
        return decorator


# Instancia global
safety = SafetyManager()