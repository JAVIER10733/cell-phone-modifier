"""
Wrapper de termux-api.
Requiere que el paquete termux-api esté instalado en Termux.
"""

import json
import shutil
import subprocess
from typing import Any, Dict, List, Optional, Tuple

from core.errors import TermuxError
from core.logger import logger
from core.platform_utils import is_termux


class TermuxAPI:
    """Wrapper para comandos de termux-api."""
    
    def __init__(self) -> None:
        self.available: bool = self._check_availability()
    
    def _check_availability(self) -> bool:
        """Verifica si termux-api está disponible."""
        if not is_termux():
            return False
        return shutil.which("termux-notification") is not None
    
    def require_api(self) -> None:
        """Lanza error si termux-api no está disponible."""
        if not self.available:
            raise TermuxError(
                "termux-api no está instalado. "
                "Instálalo con: pkg install termux-api"
            )
    
    def _run_command(self, args: List[str]) -> str:
        """
        Ejecuta un comando de termux-api.
        
        Args:
            args: Argumentos del comando
        
        Returns:
            str: Salida del comando
        """
        self.require_api()
        
        cmd = args
        logger.debug(f"Ejecutando termux-api: {' '.join(cmd)}")
        
        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                check=False,
                timeout=30
            )
            
            if result.returncode != 0:
                raise TermuxError(f"Error en termux-api: {result.stderr}")
            
            return result.stdout.strip()
        
        except subprocess.TimeoutExpired:
            raise TermuxError("Timeout en comando termux-api")
        except FileNotFoundError:
            raise TermuxError("Comando termux-api no encontrado")
    
    def send_notification(
        self,
        title: str,
        content: str,
        priority: str = "default",
        id: Optional[str] = None
    ) -> bool:
        """
        Envía una notificación.
        
        Args:
            title: Título de la notificación
            content: Contenido
            priority: Prioridad (low, default, high)
            id: ID único para actualizar notificaciones existentes
        
        Returns:
            bool: True si fue exitoso
        """
        args = [
            "termux-notification",
            "--title", title,
            "--content", content,
            "--priority", priority,
        ]
        
        if id:
            args.extend(["--id", id])
        
        try:
            self._run_command(args)
            return True
        except TermuxError as e:
            logger.error(f"Error enviando notificación: {e}")
            return False
    
    def get_battery_info(self) -> Dict[str, Any]:
        """
        Obtiene información de la batería.
        
        Returns:
            Dict[str, Any]: Información de la batería
        """
        try:
            output = self._run_command(["termux-battery-status"])
            return json.loads(output)
        except (TermuxError, json.JSONDecodeError) as e:
            logger.error(f"Error obteniendo batería: {e}")
            return {}
    
    def get_clipboard(self) -> str:
        """Obtiene el contenido del portapapeles."""
        try:
            return self._run_command(["termux-clipboard-get"])
        except TermuxError as e:
            logger.error(f"Error obteniendo portapapeles: {e}")
            return ""
    
    def set_clipboard(self, text: str) -> bool:
        """Establece el contenido del portapapeles."""
        try:
            self._run_command(["termux-clipboard-set", text])
            return True
        except TermuxError as e:
            logger.error(f"Error estableciendo portapapeles: {e}")
            return False
    
    def get_location(self, provider: str = "gps") -> Dict[str, Any]:
        """
        Obtiene la ubicación del dispositivo.
        
        Args:
            provider: Proveedor (gps, network, passive)
        
        Returns:
            Dict[str, Any]: Ubicación
        """
        try:
            output = self._run_command(["termux-location", "-p", provider])
            return json.loads(output)
        except (TermuxError, json.JSONDecodeError) as e:
            logger.error(f"Error obteniendo ubicación: {e}")
            return {}
    
    def get_wifi_info(self) -> Dict[str, Any]:
        """Obtiene información de WiFi."""
        try:
            output = self._run_command(["termux-wifi-connectioninfo"])
            return json.loads(output)
        except (TermuxError, json.JSONDecodeError) as e:
            logger.error(f"Error obteniendo WiFi: {e}")
            return {}
    
    def get_cellular_info(self) -> Dict[str, Any]:
        """Obtiene información de red celular."""
        try:
            output = self._run_command(["termux-telephony-cellinfo"])
            return json.loads(output)
        except (TermuxError, json.JSONDecodeError) as e:
            logger.error(f"Error obteniendo celular: {e}")
            return {}
    
    def vibrate(self, duration_ms: int = 1000) -> bool:
        """
        Hace vibrar el dispositivo.
        
        Args:
            duration_ms: Duración en milisegundos
        
        Returns:
            bool: True si fue exitoso
        """
        try:
            self._run_command(["termux-vibrate", "-d", str(duration_ms)])
            return True
        except TermuxError as e:
            logger.error(f"Error vibrando: {e}")
            return False
    
    def toast(self, message: str) -> bool:
        """
        Muestra un toast (mensaje emergente breve).
        
        Args:
            message: Mensaje a mostrar
        
        Returns:
            bool: True si fue exitoso
        """
        try:
            self._run_command(["termux-toast", message])
            return True
        except TermuxError as e:
            logger.error(f"Error mostrando toast: {e}")
            return False
    
    def open_url(self, url: str) -> bool:
        """Abre una URL en el navegador."""
        try:
            self._run_command(["termux-open-url", url])
            return True
        except TermuxError as e:
            logger.error(f"Error abriendo URL: {e}")
            return False


# Instancia global
termux_api = TermuxAPI()