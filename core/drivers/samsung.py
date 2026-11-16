"""
Driver para Samsung (One UI).
"""

from typing import Any, Dict, List

from core.drivers.base import BaseDriver
from core.logger import logger


class SamsungDriver(BaseDriver):
    """Driver para Samsung."""
    
    brand = "samsung"
    fastboot_mode_key = "vol_down + vol_up + conectar USB (Odin/Download)"
    recovery_mode_key = "vol_up + power + Bixby (si aplica)"
    
    def get_brand_info(self) -> Dict[str, Any]:
        return {
            "brand": "samsung",
            "type": "oneui",
            "notes": "Samsung usa Odin en lugar de fastboot estándar",
            "knox_warning": "Root rompe Knox permanentemente"
        }
    
    def get_known_issues(self) -> List[str]:
        return [
            "Samsung usa Odin en lugar de fastboot",
            "Knox se rompe permanentemente con root (0x1)",
            "Samsung Pay y Secure Folder no funcionan si Knox está roto",
            "Garantía se pierde al hacer root",
            "Algunos modelos tienen bootloader bloqueado en ciertas regiones"
        ]
    
    def get_safe_packages(self) -> List[str]:
        return [
            "com.samsung.android.bixby.agent",
            "com.samsung.android.bixby.service",
            "com.samsung.android.app.spage",
            "com.samsung.android.game.gamehome",
            "com.sec.android.app.sbrowser"
        ]
    
    def get_protected_packages(self) -> List[str]:
        return [
            "com.samsung.android.providers.context",
            "com.samsung.android.app.telephonyui",
            "com.samsung.android.incallui",
            "com.android.phone",
            "com.samsung.android.app.contacts",
            "com.samsung.android.messaging",
            "com.sec.android.app.launcher"
        ]