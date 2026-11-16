"""
Wrapper de Fastboot para cell_phone_modifier.
Ejecuta comandos Fastboot de forma segura con subprocess.
"""

import subprocess
from typing import List, Optional

from core.config import config
from core.errors import FastbootError
from core.logger import logger


class FastbootWrapper:
    """Wrapper para ejecutar comandos Fastboot."""
    
    def __init__(self, serial: Optional[str] = None) -> None:
        """
        Inicializa el wrapper de Fastboot.
        
        Args:
            serial: Serial del dispositivo (opcional)
        """
        self.serial = serial
        self.timeout = config.get("fastboot.timeout", 30)
    
    def _build_command(self, args: List[str]) -> List[str]:
        """
        Construye el comando Fastboot con serial si está especificado.
        
        Args:
            args: Argumentos del comando Fastboot
        
        Returns:
            List[str]: Comando completo
        """
        cmd = ["fastboot"]
        
        if self.serial:
            cmd.extend(["-s", self.serial])
        
        cmd.extend(args)
        return cmd
    
    def _execute(
        self,
        args: List[str],
        capture_output: bool = True,
        check: bool = True,
        timeout: Optional[int] = None
    ) -> subprocess.CompletedProcess:
        """
        Ejecuta un comando Fastboot.
        
        Args:
            args: Argumentos del comando
            capture_output: Si True, captura stdout y stderr
            check: Si True, lanza excepción si el comando falla
            timeout: Timeout en segundos
        
        Returns:
            subprocess.CompletedProcess: Resultado del comando
        
        Raises:
            FastbootError: Si el comando falla
        """
        cmd = self._build_command(args)
        timeout = timeout or self.timeout
        
        logger.debug(f"Ejecutando: {' '.join(cmd)}")
        
        try:
            result = subprocess.run(
                cmd,
                capture_output=capture_output,
                text=True,
                check=False,
                timeout=timeout
            )
            
            if check and result.returncode != 0:
                error_msg = result.stderr.strip() or result.stdout.strip()
                raise FastbootError(f"Comando Fastboot falló: {error_msg}")
            
            return result
        
        except subprocess.TimeoutExpired:
            raise FastbootError(f"Comando Fastboot agotó tiempo después de {timeout}s")
        except FileNotFoundError:
            raise FastbootError("Fastboot no encontrado. Instala con: pkg install android-tools")
        except Exception as e:
            raise FastbootError(f"Error al ejecutar Fastboot: {e}")
    
    def get_devices(self) -> List[str]:
        """
        Obtiene lista de dispositivos en modo Fastboot.
        
        Returns:
            List[str]: Lista de seriales de dispositivos
        """
        result = self._execute(["devices"], check=False)
        
        devices = []
        lines = result.stdout.strip().split('\n')
        
        for line in lines:
            if not line.strip():
                continue
            
            parts = line.split()
            if len(parts) >= 2 and parts[1] == "fastboot":
                devices.append(parts[0])
        
        return devices
    
    def get_var(self, var: str) -> str:
        """
        Obtiene una variable de Fastboot.
        
        Args:
            var: Nombre de la variable (ej: "product", "serialno")
        
        Returns:
            str: Valor de la variable
        """
        result = self._execute(["getvar", var], check=False)
        
        # Fastboot devuelve el valor en stderr
        output = result.stderr.strip()
        
        for line in output.split('\n'):
            if var in line:
                parts = line.split(':', 1)
                if len(parts) == 2:
                    return parts[1].strip()
        
        return ""
    
    def reboot(self, mode: str = "") -> bool:
        """
        Reinicia el dispositivo desde Fastboot.
        
        Args:
            mode: Modo de reinicio ("", "bootloader", "recovery")
        
        Returns:
            bool: True si fue exitoso
        """
        args = ["reboot"]
        if mode:
            args.append(mode)
        
        result = self._execute(args, check=False)
        return result.returncode == 0
    
    def flash(self, partition: str, image_path: str) -> bool:
        """
        Flashea una imagen en una partición.
        
        Args:
            partition: Nombre de la partición (ej: "boot", "recovery")
            image_path: Ruta de la imagen
        
        Returns:
            bool: True si fue exitoso
        """
        result = self._execute(["flash", partition, image_path], check=False, timeout=120)
        return result.returncode == 0
    
    def erase(self, partition: str) -> bool:
        """
        Borra una partición.
        
        Args:
            partition: Nombre de la partición
        
        Returns:
            bool: True si fue exitoso
        """
        result = self._execute(["erase", partition], check=False)
        return result.returncode == 0
    
    def set_serial(self, serial: str) -> None:
        """
        Establece el serial del dispositivo.
        
        Args:
            serial: Serial del dispositivo
        """
        self.serial = serial
        logger.info(f"Serial Fastboot establecido: {serial}")