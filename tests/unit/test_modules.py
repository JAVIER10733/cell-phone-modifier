"""
Tests para los módulos base y registry.
"""

from unittest.mock import MagicMock

import pytest

from core.errors import DeviceError
from core.modules.base import BaseModule
from core.modules.registry import ModuleRegistry, registry


class TestModuleRegistry:
    def test_registrar_modulo(self):
        reg = ModuleRegistry()
        
        class TestModule(BaseModule):
            name = "test_module"
            description = "Módulo de prueba"
            requires_device = False
            
            def execute(self, **kwargs):
                return "ok"
        
        reg.register(TestModule)
        assert reg.get("test_module") is TestModule
    
    def test_registrar_no_base_module(self):
        reg = ModuleRegistry()
        
        class NotAModule:
            pass
        
        with pytest.raises(Exception):
            reg.register(NotAModule)
    
    def test_list_modules(self):
        reg = ModuleRegistry()
        
        class TestModule(BaseModule):
            name = "test"
            description = "Test"
            requires_device = False
            
            def execute(self, **kwargs):
                return None
        
        reg.register(TestModule)
        modules = reg.list_modules()
        assert len(modules) == 1
        assert modules[0]["name"] == "test"
    
    def test_global_registry(self):
        # El registry global debe tener módulos registrados
        modules = registry.list_modules()
        assert len(modules) > 0


class TestBaseModule:
    def test_verify_device_conectado(self, mock_adb_wrapper):
        class DummyModule(BaseModule):
            name = "dummy"
            description = "Dummy"
            requires_device = True
            
            def execute(self, **kwargs):
                return "ok"
        
        module = DummyModule(adb=mock_adb_wrapper)
        assert module.verify_device() is True
    
    def test_verify_device_no_conectado(self):
        class DummyModule(BaseModule):
            name = "dummy"
            description = "Dummy"
            requires_device = True
            
            def execute(self, **kwargs):
                return "ok"
        
        mock_adb = MagicMock()
        mock_adb.get_devices.return_value = []
        mock_adb.serial = None
        
        module = DummyModule(adb=mock_adb)
        with pytest.raises(DeviceError):
            module.verify_device()
    
    def test_get_info(self, mock_adb_wrapper):
        class DummyModule(BaseModule):
            name = "dummy"
            description = "Dummy module"
            requires_device = False
            requires_root = False
            danger_level = "low"
            
            def execute(self, **kwargs):
                return None
        
        module = DummyModule(adb=mock_adb_wrapper)
        info = module.get_info()
        
        assert info["name"] == "dummy"
        assert info["description"] == "Dummy module"
        assert info["requires_device"] is False