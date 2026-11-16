"""
Módulo de excepciones personalizadas para cell_phone_modifier.
Todas las excepciones heredan de CellPhoneModifierError para facilitar el manejo.
"""

from typing import Optional


class CellPhoneModifierError(Exception):
    """Excepción base para todos los errores del proyecto."""

    def __init__(self, message: str, code: Optional[str] = None) -> None:
        super().__init__(message)
        self.message = message
        self.code = code

    def __str__(self) -> str:
        if self.code:
            return f"[{self.code}] {self.message}"
        return self.message


class TermuxError(CellPhoneModifierError):
    """Error relacionado con el entorno de Termux."""
    pass


class DependencyError(CellPhoneModifierError):
    """Error cuando falta una dependencia (adb, fastboot, python, etc.)."""
    pass


class ConfigError(CellPhoneModifierError):
    """Error en la configuración (JSON inválido, .env faltante, etc.)."""
    pass


class ADBError(CellPhoneModifierError):
    """Error en la ejecución de comandos ADB."""
    pass


class FastbootError(CellPhoneModifierError):
    """Error en la ejecución de comandos Fastboot."""
    pass


class DeviceError(CellPhoneModifierError):
    """Error relacionado con el dispositivo (desconectado, no autorizado, etc.)."""
    pass


class SafetyError(CellPhoneModifierError):
    """Error de seguridad (acción destructiva sin confirmación, root requerido, etc.)."""
    pass


class ValidationError(CellPhoneModifierError):
    """Error de validación de entrada (serial inválido, IP incorrecta, etc.)."""
    pass


class StorageError(CellPhoneModifierError):
    """Error de almacenamiento (espacio insuficiente, permisos denegados, etc.)."""
    pass


class TimeoutError(CellPhoneModifierError):
    """Error de timeout en operaciones de red o dispositivo."""
    pass