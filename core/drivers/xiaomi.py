"""
Driver para Xiaomi/Redmi/POCO (MIUI/HyperOS).
"""

from typing import Any, Dict, List

from core.drivers.base import BaseDriver
from core.logger import logger


class XiaomiDriver(BaseDriver):
    """Driver para Xiaomi."""
    
    brand = "xiaomi"
    fastboot_mode_key = "vol_down + power"
    recovery_mode_key = "vol_up + power"
    
    def get_brand_info(self) -> Dict[str, Any]:
        return {
            "brand": "xiaomi",
            "type": "miui",
            "notes": "Requiere cuenta Mi para desbloquear bootloader",
            "unlock_wait": "7-30 días de espera obligatoria"
        }
    
    def get_known_issues(self) -> List[str]:
        return [
            "Desbloqueo de bootloader requiere cuenta Mi y espera de 7-30 días",
            "MIUI tiene muchas apps de bloatware",
            "HyperOS (MIUI 15+) tiene restricciones adicionales",
            "Algunos modelos tienen Anti-Rollback (no flashear versiones inferiores)",
            "MSA (sistema de anuncios) está integrado profundamente"
        ]
    
    def get_safe_packages(self) -> List[str]:
        return [
            "com.miui.analytics",
            "com.miui.msa.global",
            "com.miui.hybrid",
            "com.xiaomi.gamecenter",
            "com.xiaomi.mipicks",
            "com.xiaomi.shop",
            "com.facebook.katana",
            "com.facebook.services"
        ]
    
    def get_protected_packages(self) -> List[str]:
        return [
            "com.miui.securitycenter",
            "com.miui.securityadd",
            "com.miui.guardprovider",
            "com.xiaomi.finddevice",
            "com.xiaomi.xmsf",
            "com.xiaomi.xmsfkeeper",
            "com.android.phone",
            "com.miui.home",
            "com.miui.packageinstaller"
        ]