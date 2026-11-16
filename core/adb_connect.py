"""
Flujo de conexión ADB inalámbrica (pair y connect).
"""

import re
from typing import Dict, Optional, Tuple

from core.adb_wrapper import ADBWrapper
from core.errors import ADBError, DeviceError
from core.logger import logger
from core.validators import validate_ip, validate_port


class ADBConnect:
    """Gestiona la conexión ADB inalámbrica."""
    
    def __init__(self, adb: Optional[ADBWrapper] = None) -> None:
        self.adb = adb or ADBWrapper()
    
    def pair(
        self,
        host: str,
        port: int,
        code: str
    ) -> Tuple[bool, str]:
        """
        Empareja con un dispositivo Android 11+ usando código de pairing.
        
        Args:
            host: IP del dispositivo
            port: Puerto de pairing
            code: Código de 6 dígitos
        
        Returns:
            Tuple[bool, str]: (éxito, mensaje)
        """
        # Validar IP
        ip_valid, ip_msg = validate_ip(host)
        if not ip_valid:
            return False, f"IP inválida: {ip_msg}"
        
        # Validar puerto
        port_valid, port_msg = validate_port(port)
        if not port_valid:
            return False, f"Puerto inválido: {port_msg}"
        
        # Validar código
        if not code or len(code) != 6 or not code.isdigit():
            return False, "Código debe ser de 6 dígitos numéricos"
        
        logger.info(f"Emparejando con {host}:{port}...")
        
        try:
            result = self.adb._execute(
                ["pair", f"{host}:{port}", code],
                check=False
            )
            
            output = result.stdout + result.stderr
            
            if "Successfully paired" in output:
                logger.info("Emparejamiento exitoso")
                return True, "Emparejamiento exitoso"
            
            if "invalid" in output.lower() or "failed" in output.lower():
                return False, f"Emparejamiento falló: {output.strip()}"
            
            return True, output.strip()
        
        except Exception as e:
            logger.error(f"Error en pairing: {e}")
            return False, str(e)
    
    def connect(
        self,
        host: str,
        port: int = 5555
    ) -> Tuple[bool, str]:
        """
        Conecta a un dispositivo por WiFi.
        
        Args:
            host: IP del dispositivo
            port: Puerto (default: 5555)
        
        Returns:
            Tuple[bool, str]: (éxito, mensaje)
        """
        ip_valid, ip_msg = validate_ip(host)
        if not ip_valid:
            return False, f"IP inválida: {ip_msg}"
        
        port_valid, port_msg = validate_port(port)
        if not port_valid:
            return False, f"Puerto inválido: {port_msg}"
        
        logger.info(f"Conectando a {host}:{port}...")
        
        try:
            result = self.adb._execute(
                ["connect", f"{host}:{port}"],
                check=False
            )
            
            output = result.stdout.strip()
            
            if "connected" in output.lower():
                self.adb.set_serial(f"{host}:{port}")
                logger.info(f"Conectado a {host}:{port}")
                return True, output
            
            if "refused" in output.lower():
                return False, "Conexión rechazada. Verifica que ADB WiFi esté activado en el dispositivo"
            
            if "timeout" in output.lower():
                return False, "Timeout. Verifica la IP y que el dispositivo esté en la misma red"
            
            return False, output
        
        except Exception as e:
            logger.error(f"Error conectando: {e}")
            return False, str(e)
    
    def disconnect(self, target: Optional[str] = None) -> Tuple[bool, str]:
        """
        Desconecta un dispositivo.
        
        Args:
            target: Serial o IP:puerto. Si es None, desconecta todos.
        
        Returns:
            Tuple[bool, str]: (éxito, mensaje)
        """
        args = ["disconnect"]
        if target:
            args.append(target)
        
        try:
            result = self.adb._execute(args, check=False)
            output = result.stdout.strip()
            logger.info(f"Desconectado: {output}")
            return True, output
        except Exception as e:
            logger.error(f"Error desconectando: {e}")
            return False, str(e)
    
    def enable_wifi_adb(self) -> Tuple[bool, str]:
        """
        Activa ADB por WiFi en el dispositivo (requiere USB primero).
        
        Returns:
            Tuple[bool, str]: (éxito, mensaje)
        """
        logger.info("Activando ADB WiFi en puerto 5555...")
        
        try:
            result = self.adb._execute(["tcpip", "5555"], check=False)
            output = result.stdout.strip()
            
            if "restarting" in output.lower() or "5555" in output:
                logger.info("ADB WiFi activado")
                return True, "ADB WiFi activado. Ahora puedes desconectar el USB"
            
            return False, output
        
        except Exception as e:
            logger.error(f"Error activando ADB WiFi: {e}")
            return False, str(e)
    
    def get_device_ip(self) -> Optional[str]:
        """
        Obtiene la IP del dispositivo conectado por USB.
        
        Returns:
            Optional[str]: IP del dispositivo o None
        """
        try:
            # Intentar obtener IP de WiFi
            ip = self.adb.shell("ip addr show wlan0 | grep 'inet ' | awk '{print $2}' | cut -d/ -f1")
            if ip and ip != "":
                return ip
            
            # Fallback a ip route
            ip = self.adb.shell("ip route | grep wlan0 | awk '{print $9}'")
            if ip and ip != "":
                return ip
            
            return None
        except Exception as e:
            logger.debug(f"No se pudo obtener IP: {e}")
            return None