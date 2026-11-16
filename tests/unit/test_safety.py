"""
Tests para el módulo de seguridad.
"""

import pytest

from core.safety import SafetyManager


class TestSafetyManager:
    def test_dry_run_activado(self):
        safety = SafetyManager(dry_run=True)
        assert safety.dry_run is True
        
        # En dry-run, confirm() retorna False
        result = safety.confirm("acción de prueba", "medium")
        assert result is False
    
    def test_dry_run_desactivado(self):
        safety = SafetyManager(dry_run=False)
        assert safety.dry_run is False
    
    def test_auto_confirm(self):
        safety = SafetyManager(auto_confirm=True)
        result = safety.confirm("acción de prueba", "medium")
        assert result is True
    
    def test_confirm_critical_auto(self):
        safety = SafetyManager(auto_confirm=True)
        result = safety.confirm_critical("acción crítica")
        assert result is True
    
    def test_confirm_critical_dry_run(self):
        safety = SafetyManager(dry_run=True)
        result = safety.confirm_critical("acción crítica")
        assert result is False
    
    def test_enable_disable_dry_run(self):
        safety = SafetyManager()
        assert safety.dry_run is False
        
        safety.enable_dry_run()
        assert safety.dry_run is True
        
        safety.disable_dry_run()
        assert safety.dry_run is False
    
    def test_enable_disable_auto_confirm(self):
        safety = SafetyManager()
        assert safety.auto_confirm is False
        
        safety.enable_auto_confirm()
        assert safety.auto_confirm is True
        
        safety.disable_auto_confirm()
        assert safety.auto_confirm is False