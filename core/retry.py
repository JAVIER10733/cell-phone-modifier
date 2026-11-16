"""
Módulo de reintentos con backoff exponencial.
"""

import time
from typing import Any, Callable, Optional, Tuple, Type

from core.logger import logger


def retry_with_backoff(
    func: Callable,
    max_attempts: int = 3,
    base_delay: float = 1.0,
    max_delay: float = 30.0,
    exceptions: Tuple[Type[Exception], ...] = (Exception,),
    on_retry: Optional[Callable[[int, Exception], None]] = None
) -> Any:
    """
    Ejecuta una función con reintentos y backoff exponencial.
    
    Args:
        func: Función a ejecutar
        max_attempts: Número máximo de intentos
        base_delay: Delay inicial en segundos
        max_delay: Delay máximo en segundos
        exceptions: Tupla de excepciones a capturar
        on_retry: Callback opcional llamado antes de cada reintento
    
    Returns:
        Resultado de la función
    
    Raises:
        Exception: La última excepción si todos los intentos fallan
    """
    last_exception: Optional[Exception] = None
    
    for attempt in range(1, max_attempts + 1):
        try:
            return func()
        except exceptions as e:
            last_exception = e
            
            if attempt == max_attempts:
                logger.error(f"Fallo después de {max_attempts} intentos: {e}")
                raise
            
            # Calcular delay con backoff exponencial
            delay = min(base_delay * (2 ** (attempt - 1)), max_delay)
            
            logger.warning(
                f"Intento {attempt}/{max_attempts} falló: {e}. "
                f"Reintentando en {delay:.1f}s..."
            )
            
            if on_retry:
                on_retry(attempt, e)
            
            time.sleep(delay)
    
    # Esto no debería alcanzarse, pero por seguridad
    if last_exception:
        raise last_exception
    
    raise RuntimeError("Retry agotado sin excepción")


def retry_adb_command(
    func: Callable,
    max_attempts: int = 3,
    base_delay: float = 2.0
) -> Any:
    """
    Wrapper específico para comandos ADB con reintentos.
    
    Args:
        func: Función que ejecuta el comando ADB
        max_attempts: Número máximo de intentos
        base_delay: Delay inicial en segundos
    
    Returns:
        Resultado del comando
    """
    from core.errors import ADBError, DeviceError, TimeoutError
    
    return retry_with_backoff(
        func,
        max_attempts=max_attempts,
        base_delay=base_delay,
        max_delay=10.0,
        exceptions=(ADBError, DeviceError, TimeoutError)
    )