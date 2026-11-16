"""
Wrapper de ADB para cell_phone_modifier.
Ejecuta comandos ADB de forma segura con subprocess.
"""

import subprocess
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from core.config import config
from core.errors import ADBError, DeviceError, TimeoutError
from core.logger import logger
from core.retry import retry_adb_command
from core.validators import validate_serial


class ADBWrapper:
    """Wrapper para ejecutar comandos ADB."""
    
    def __init__(self, serial: Optional[str] = None) -> None:
        """
        Inicializa el wrapper de ADB.
        
        Args:
            serial: Serial del dispositivo (opcional)
        """
        self.serial = serial
        self.timeout = config.get("adb.timeout", 30)
        self.retry_attempts = config.get("adb.retry_attempts", 3)
        self.retry_delay = config.get("adb.retry_delay", 2)
    
    def _build_command(self, args: List[str]) -> List[str]:
        """
        Construye el comando ADB con serial si está especificado.
        
        Args:
            args: Argumentos del comando ADB
        
        Returns:
            List[str]: Comando completo
        """
        cmd = ["adb"]
        
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
        Ejecuta un comando ADB.
        
        Args:
            args: Argumentos del comando
            capture_output: Si True, captura stdout y stderr
            check: Si True, lanza excepción si el comando falla
            timeout: Timeout en segundos
        
        Returns:
            subprocess.CompletedProcess: Resultado del comando
        
        Raises:
            ADBError: Si el comando falla
            TimeoutError: Si se agota el tiempo
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
                
                # Detectar errores comunes
                if "device not found" in error_msg.lower():
                    raise DeviceError(f"Dispositivo no encontrado: {self.serial}")
                
                if "unauthorized" in error_msg.lower():
                    raise DeviceError(
                        f"Dispositivo no autorizado: {self.serial}. "
                        "Acepta la solicitud en el dispositivo."
                    )
                
                if "offline" in error_msg.lower():
                    raise DeviceError(f"Dispositivo offline: {self.serial}")
                
                raise ADBError(f"Comando ADB falló: {error_msg}")
            
            return result
        
        except subprocess.TimeoutExpired:
            raise TimeoutError(f"Comando ADB agotó tiempo después de {timeout}s")
        except FileNotFoundError:
            raise ADBError("ADB no encontrado. Instala con: pkg install android-tools")
        except Exception as e:
            raise ADBError(f"Error al ejecutar ADB: {e}")
    
    def execute_with_retry(
        self,
        args: List[str],
        max_attempts: Optional[int] = None
    ) -> subprocess.CompletedProcess:
        """
        Ejecuta un comando ADB con reintentos.
        
        Args:
            args: Argumentos del comando
            max_attempts: Número máximo de intentos
        
        Returns:
            subprocess.CompletedProcess: Resultado del comando
        """
        max_attempts = max_attempts or self.retry_attempts
        
        def execute():
            return self._execute(args)
        
        return retry_adb_command(execute, max_attempts=max_attempts, base_delay=self.retry_delay)
    
    def get_devices(self) -> List[Dict[str, str]]:
        """
        Obtiene lista de dispositivos conectados.
        
        Returns:
            List[Dict[str, str]]: Lista de dispositivos con serial y estado
        """
        result = self._execute(["devices", "-l"], check=False)
        
        devices = []
        lines = result.stdout.strip().split('\n')[1:]  # Saltar primera línea
        
        for line in lines:
            if not line.strip():
                continue
            
            parts = line.split()
            if len(parts) >= 2:
                serial = parts[0]
                state = parts[1]
                
                device_info = {
                    "serial": serial,
                    "state": state
                }
                
                # Parsear información adicional
                for part in parts[2:]:
                    if ':' in part:
                        key, value = part.split(':', 1)
                        device_info[key] = value
                
                devices.append(device_info)
        
        return devices
    
    def is_device_connected(self) -> bool:
        """
        Verifica si el dispositivo está conectado.
        
        Returns:
            bool: True si está conectado y autorizado
        """
        if not self.serial:
            return False
        
        devices = self.get_devices()
        
        for device in devices:
            if device["serial"] == self.serial and device["state"] == "device":
                return True
        
        return False
    
    def get_property(self, prop: str) -> str:
        """
        Obtiene una propiedad del dispositivo.
        
        Args:
            prop: Nombre de la propiedad (ej: "ro.product.model")
        
        Returns:
            str: Valor de la propiedad
        """
        result = self._execute(["shell", "getprop", prop])
        return result.stdout.strip()
    
    def shell(self, command: str, check: bool = True) -> str:
        """
        Ejecuta un comando shell en el dispositivo.
        
        Args:
            command: Comando a ejecutar
            check: Si True, lanza excepción si falla
        
        Returns:
            str: Salida del comando
        """
        result = self._execute(["shell", command], check=check)
        return result.stdout.strip()
    
    def pull(self, remote_path: str, local_path: str) -> bool:
        """
        Copia un archivo del dispositivo al PC.
        
        Args:
            remote_path: Ruta en el dispositivo
            local_path: Ruta local de destino
        
        Returns:
            bool: True si fue exitoso
        """
        result = self._execute(["pull", remote_path, local_path], check=False)
        return result.returncode == 0
    
    def push(self, local_path: str, remote_path: str) -> bool:
        """
        Copia un archivo del PC al dispositivo.
        
        Args:
            local_path: Ruta local del archivo
            remote_path: Ruta de destino en el dispositivo
        
        Returns:
            bool: True si fue exitoso
        """
        if not Path(local_path).exists():
            raise ADBError(f"Archivo local no existe: {local_path}")
        
        result = self._execute(["push", local_path, remote_path], check=False)
        return result.returncode == 0
    
    def install(self, apk_path: str, replace: bool = False) -> bool:
        """
        Instala una APK en el dispositivo.
        
        Args:
            apk_path: Ruta local de la APK
            replace: Si True, reemplaza la app si ya existe
        
        Returns:
            bool: True si fue exitoso
        """
        if not Path(apk_path).exists():
            raise ADBError(f"APK no existe: {apk_path}")
        
        args = ["install"]
        if replace:
            args.append("-r")
        args.append(apk_path)
        
        result = self._execute(args, check=False, timeout=120)
        return result.returncode == 0
    
    def uninstall(self, package: str, keep_data: bool = False) -> bool:
        """
        Desinstala una app del dispositivo.
        
        Args:
            package: Nombre del paquete
            keep_data: Si True, mantiene los datos de la app
        
        Returns:
            bool: True si fue exitoso
        """
        args = ["uninstall"]
        if keep_data:
            args.append("-k")
        args.append(package)
        
        result = self._execute(args, check=False)
        return result.returncode == 0
    
    def reboot(self, mode: str = "") -> bool:
        """
        Reinicia el dispositivo.
        
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
    
    def set_serial(self, serial: str) -> None:
        """
        Establece el serial del dispositivo.
        
        Args:
            serial: Serial del dispositivo
        
        Raises:
            ADBError: Si el serial es inválido
        """
        valid, msg = validate_serial(serial)
        if not valid:
            raise ADBError(f"Serial inválido: {msg}")
        
        self.serial = serial
        logger.info(f"Serial establecido: {serial}")