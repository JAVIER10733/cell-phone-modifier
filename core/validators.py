"""
Validadores para cell_phone_modifier.
Valida seriales de dispositivos, IPs, puertos y rutas.
"""

import re
from pathlib import Path
from typing import Optional, Tuple

from core.errors import ValidationError


def validate_serial(serial: str) -> Tuple[bool, str]:
    """
    Valida un serial de dispositivo ADB.
    
    Args:
        serial: Serial del dispositivo (ej: "ABC123456" o "192.168.1.100:5555")
    
    Returns:
        Tuple[bool, str]: (válido, mensaje)
    """
    if not serial or not isinstance(serial, str):
        return False, "Serial vacío o no es string"
    
    serial = serial.strip()
    
    if len(serial) < 3:
        return False, "Serial demasiado corto"
    
    if len(serial) > 100:
        return False, "Serial demasiado largo"
    
    # Permitir seriales alfanuméricos con guiones y guiones bajos
    if re.match(r'^[a-zA-Z0-9_\-:]+$', serial):
        return True, "Serial válido"
    
    return False, "Serial contiene caracteres inválidos"


def validate_ip(ip: str) -> Tuple[bool, str]:
    """
    Valida una dirección IPv4.
    
    Args:
        ip: Dirección IP (ej: "192.168.1.100")
    
    Returns:
        Tuple[bool, str]: (válido, mensaje)
    """
    if not ip or not isinstance(ip, str):
        return False, "IP vacía o no es string"
    
    ip = ip.strip()
    
    # Regex para IPv4
    pattern = r'^(\d{1,3}\.){3}\d{1,3}$'
    if not re.match(pattern, ip):
        return False, "Formato de IP inválido"
    
    # Validar rangos
    parts = ip.split('.')
    for part in parts:
        try:
            num = int(part)
            if num < 0 or num > 255:
                return False, f"Octeto {num} fuera de rango (0-255)"
        except ValueError:
            return False, "IP contiene valores no numéricos"
    
    return True, "IP válida"


def validate_port(port: int) -> Tuple[bool, str]:
    """
    Valida un número de puerto.
    
    Args:
        port: Número de puerto (1-65535)
    
    Returns:
        Tuple[bool, str]: (válido, mensaje)
    """
    if not isinstance(port, int):
        return False, "Puerto debe ser entero"
    
    if port < 1 or port > 65535:
        return False, "Puerto fuera de rango (1-65535)"
    
    return True, "Puerto válido"


def validate_path(path: str, must_exist: bool = False, create: bool = False) -> Tuple[bool, str, Optional[Path]]:
    """
    Valida una ruta de archivo o directorio.
    
    Args:
        path: Ruta a validar
        must_exist: Si True, la ruta debe existir
        create: Si True, crea la ruta si no existe
    
    Returns:
        Tuple[bool, str, Optional[Path]]: (válido, mensaje, ruta_resuelta)
    """
    if not path or not isinstance(path, str):
        return False, "Ruta vacía o no es string", None
    
    try:
        path_obj = Path(path).expanduser().resolve()
        
        if must_exist and not path_obj.exists():
            return False, f"La ruta no existe: {path_obj}", None
        
        if create and not path_obj.exists():
            try:
                path_obj.mkdir(parents=True, exist_ok=True)
                return True, f"Ruta creada: {path_obj}", path_obj
            except Exception as e:
                return False, f"Error al crear ruta: {e}", None
        
        return True, "Ruta válida", path_obj
    
    except Exception as e:
        return False, f"Error al validar ruta: {e}", None


def validate_host_port(host: str, port: int) -> Tuple[bool, str]:
    """
    Valida una combinación host:puerto para ADB inalámbrico.
    
    Args:
        host: Dirección IP o hostname
        port: Número de puerto
    
    Returns:
        Tuple[bool, str]: (válido, mensaje)
    """
    ip_valid, ip_msg = validate_ip(host)
    if not ip_valid:
        return False, ip_msg
    
    port_valid, port_msg = validate_port(port)
    if not port_valid:
        return False, port_msg
    
    return True, "Host y puerto válidos"


def validate_serial_or_ip(target: str) -> Tuple[bool, str, str]:
    """
    Valida si es un serial de dispositivo o una IP:puerto.
    
    Args:
        target: Serial o IP:puerto
    
    Returns:
        Tuple[bool, str, str]: (válido, tipo, mensaje)
        tipo: "serial" o "ip_port"
    """
    if not target or not isinstance(target, str):
        return False, "", "Target vacío o no es string"
    
    target = target.strip()
    
    # Verificar si es IP:puerto
    if ':' in target:
        parts = target.split(':')
        if len(parts) == 2:
            host, port_str = parts
            ip_valid, ip_msg = validate_ip(host)
            if not ip_valid:
                return False, "", ip_msg
            
            try:
                port = int(port_str)
                port_valid, port_msg = validate_port(port)
                if not port_valid:
                    return False, "", port_msg
                return True, "ip_port", "IP:puerto válido"
            except ValueError:
                return False, "", "Puerto no es numérico"
    
    # Verificar si es serial
    serial_valid, serial_msg = validate_serial(target)
    if serial_valid:
        return True, "serial", "Serial válido"
    
    return False, "", "No es serial ni IP:puerto válido"