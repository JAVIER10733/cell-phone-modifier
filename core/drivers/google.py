"""
Driver para Google Pixel (Android puro).
"""

from typing import Any, Dict, List

from core.drivers.base import BaseDriver
from core.logger import logger


class GoogleDriver(BaseDriver):
    """Driver para Google Pixel."""
    
    brand = "google"
    fastboot_mode_key = "vol_down + power"
    recovery_mode_key = "vol_up + power"
    
    def get_brand_info(self) -> Dict[str, Any]:
        return {
            "brand": "google",
            "type": "stock",
            "notes": "Android puro, recibe actualizaciones primero",
            "fastboot": "Usa 'fastboot flashing unlock' en lugar de 'fastboot oem unlock'"
        }
    
    def get_known_issues(self) -> List[str]:
        return [
            "Desbloquear bootloader muestra advertencia en cada arranque",
            "Desbloquear bootloader hace factory reset",
            "Google Play Services es esencial, no desactivar",
            "Algunos sensores (SPO2, temperatura) solo en modelos Pro",
            "Factory images disponibles en developers.google.com/android"
        ]
    
    def get_safe_packages(self) -> List[str]:
        return [
            "com.google.android.apps.tachyon",
            "com.google.android.apps.magazines",
            "com.google.android.apps.books",
            "com.google.android.apps.fitness",
            "com.google.android.apps.photosgo",
            "com.google.android.apps.navlite",
            "com.google.android.apps.translate"
        ]
    
    def get_protected_packages(self) -> List[str]:
        return [
            "com.google.android.gms",
            "com.google.android.gsf",
            "com.google.android.onetimeinitializer",
            "com.google.android.setupwizard",
            "com.android.phone",
            "com.google.android.dialer",
            "com.google.android.apps.messaging"
        ]