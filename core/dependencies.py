"""
Módulo para verificar dependencias del sistema.
Verifica que adb, fastboot, python y otras herramientas estén disponibles.
"""

import shutil
from pathlib import Path
from typing import Dict, List, Optional, Tuple

from core.errors import DependencyError, TermuxError
from core.logger import logger
from core.platform_utils import is_termux


class DependencyChecker:
    """Verifica que todas las dependencias necesarias estén instaladas."""
    
    def __init__(self) -> None:
        self.results: Dict[str, Tuple[bool, str]] = {}
    
    def check_python(self) -> Tuple[bool, str]:
        """
        Verifica que Python esté disponible.
        
        Returns:
            Tuple[bool, str]: (disponible, mensaje)
        """
        python_path = shutil.which("python")
        if python_path:
            return True, f"Python encontrado en {python_path}"
        return False, "Python no encontrado. Instala con: pkg install python"
    
    def check_adb(self) -> Tuple[bool, str]:
        """
        Verifica que ADB esté disponible.
        
        Returns:
            Tuple[bool, str]: (disponible, mensaje)
        """
        adb_path = shutil.which("adb")
        if adb_path:
            return True, f"ADB encontrado en {adb_path}"
        return False, "ADB no encontrado. Instala con: pkg install android-tools"
    
    def check_fastboot(self) -> Tuple[bool, str]:
        """
        Verifica que Fastboot esté disponible.
        
        Returns:
            Tuple[bool, str]: (disponible, mensaje)
        """
        fastboot_path = shutil.which("fastboot")
        if fastboot_path:
            return True, f"Fastboot encontrado en {fastboot_path}"
        return False, "Fastboot no encontrado. Instala con: pkg install android-tools"
    
    def check_git(self) -> Tuple[bool, str]:
        """
        Verifica que Git esté disponible.
        
        Returns:
            Tuple[bool, str]: (disponible, mensaje)
        """
        git_path = shutil.which("git")
        if git_path:
            return True, f"Git encontrado en {git_path}"
        return False, "Git no encontrado. Instala con: pkg install git"
    
    def check_termux_api(self) -> Tuple[bool, str]:
        """
        Verifica que termux-api esté disponible (opcional).
        
        Returns:
            Tuple[bool, str]: (disponible, mensaje)
        """
        if not is_termux():
            return False, "No está en Termux."
        
        termux_api_path = shutil.which("termux-notification")
        if termux_api_path:
            return True, "termux-api disponible"
        return False, "termux-api no encontrado. Instala con: pkg install termux-api (opcional)"
    
    def check_all(self) -> Dict[str, Tuple[bool, str]]:
        """
        Verifica todas las dependencias.
        
        Returns:
            Dict[str, Tuple[bool, str]]: Resultados de verificación.
        """
        self.results = {
            "python": self.check_python(),
            "adb": self.check_adb(),
            "fastboot": self.check_fastboot(),
            "git": self.check_git(),
        }
        
        if is_termux():
            self.results["termux_api"] = self.check_termux_api()
        
        return self.results
    
    def get_missing(self) -> List[str]:
        """
        Retorna lista de dependencias faltantes.
        
        Returns:
            List[str]: Nombres de dependencias faltantes.
        """
        if not self.results:
            self.check_all()
        
        return [name for name, (available, _) in self.results.items() if not available]
    
    def require(self, dependencies: List[str]) -> None:
        """
        Verifica que las dependencias especificadas estén disponibles.
        
        Args:
            dependencies: Lista de dependencias requeridas.
        
        Raises:
            DependencyError: Si falta alguna dependencia requerida.
        """
        if not self.results:
            self.check_all()
        
        missing = []
        for dep in dependencies:
            if dep not in self.results:
                missing.append(dep)
            elif not self.results[dep][0]:
                missing.append(f"{dep}: {self.results[dep][1]}")
        
        if missing:
            error_msg = "Dependencias faltantes:\n" + "\n".join(f"  - {m}" for m in missing)
            raise DependencyError(error_msg)
    
    def print_status(self) -> None:
        """Imprime el estado de todas las dependencias."""
        if not self.results:
            self.check_all()
        
        print("\n=== Estado de Dependencias ===")
        for name, (available, message) in self.results.items():
            status = "✅" if available else "❌"
            print(f"{status} {name}: {message}")
        print()


# Instancia global
checker = DependencyChecker()


def check_dependencies(required: Optional[List[str]] = None) -> None:
    """
    Función de conveniencia para verificar dependencias.
    
    Args:
        required: Lista de dependencias requeridas. Si es None, verifica todas.
    
    Raises:
        DependencyError: Si falta alguna dependencia requerida.
    """
    checker.check_all()
    
    if required:
        checker.require(required)
    
    checker.print_status()
    