"""
Registro de auditoría para acciones críticas.
"""

import json
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

from core.logger import logger
from core.platform_utils import get_termux_paths, is_termux


class AuditLog:
    """Registro de auditoría para acciones críticas."""
    
    def __init__(self, log_path: Optional[Path] = None) -> None:
        if log_path:
            self.log_path = log_path
        elif is_termux():
            paths = get_termux_paths()
            self.log_path = paths["home"] / "cell_phone_modifier" / "logs" / "audit.log"
        else:
            self.log_path = Path(__file__).parent.parent / "logs" / "audit.log"
        
        self.log_path.parent.mkdir(parents=True, exist_ok=True)
    
    def log(
        self,
        action: str,
        module: str,
        details: Optional[Dict[str, Any]] = None,
        user: str = "local",
        success: bool = True
    ) -> None:
        """
        Registra una acción en el log de auditoría.
        
        Args:
            action: Descripción de la acción
            module: Módulo que ejecutó la acción
            details: Detalles adicionales
            user: Usuario que ejecutó la acción
            success: Si fue exitosa
        """
        entry = {
            "timestamp": datetime.now().isoformat(),
            "action": action,
            "module": module,
            "user": user,
            "success": success,
            "details": details or {}
        }
        
        line = json.dumps(entry, ensure_ascii=False)
        
        try:
            with open(self.log_path, "a", encoding="utf-8") as f:
                f.write(line + "\n")
            logger.debug(f"Audit: {action}")
        except Exception as e:
            logger.error(f"Error escribiendo audit log: {e}")
    
    def get_entries(
        self,
        limit: int = 100,
        module: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        Obtiene entradas del log de auditoría.
        
        Args:
            limit: Máximo de entradas
            module: Filtrar por módulo
        
        Returns:
            List[Dict[str, Any]]: Entradas del log
        """
        if not self.log_path.exists():
            return []
        
        entries = []
        try:
            with open(self.log_path, "r", encoding="utf-8") as f:
                lines = f.readlines()
            
            for line in reversed(lines):
                if not line.strip():
                    continue
                
                try:
                    entry = json.loads(line)
                    
                    if module and entry.get("module") != module:
                        continue
                    
                    entries.append(entry)
                    
                    if len(entries) >= limit:
                        break
                except json.JSONDecodeError:
                    continue
        except Exception as e:
            logger.error(f"Error leyendo audit log: {e}")
        
        return entries
    
    def clear(self) -> None:
        """Limpia el log de auditoría."""
        if self.log_path.exists():
            self.log_path.unlink()
            logger.info("Log de auditoría limpiado")


# Instancia global
audit = AuditLog()