"""
Driver genérico para cualquier Android.
"""

from typing import Any, Dict, List

from core.drivers.base import BaseDriver
from core.logger import logger


class GenericDriver(BaseDriver):
    """Driver genérico."""
    
    brand = "generic"
    
    def get_brand_info(self) -> Dict[str, Any]:
        return {
            "brand": "generic",
            "type": "aosp",
            "notes": "Driver genérico para Android estándar"
        }
    
    def get_known_issues(self) -> List[str]:
        return [
            "Algunos fabricantes modifican comandos ADB",
            "Permisos pueden variar según versión de Android"
        ]
    
    def get_safe_packages(self) -> List[str]:
        return []
    
    def get_protected_packages(self) -> List[str]:
        return [
            "com.android.phone",
            "com.android.systemui",
            "com.android.settings"
        ]