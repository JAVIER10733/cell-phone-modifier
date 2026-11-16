"""
Tests para el módulo de configuración.
"""

import json
from pathlib import Path

import pytest

from core.config import Config
from core.errors import ConfigError


class TestConfig:
    def test_cargar_config_existente(self, temp_config_dir):
        config = Config(config_dir=temp_config_dir)
        assert config.get("app.name") == "test"
        assert config.get("app.version") == "0.1.0"
        assert config.get("adb.timeout") == 10
    
    def test_config_por_defecto(self, tmp_path):
        config_dir = tmp_path / "config"
        config_dir.mkdir()
        config = Config(config_dir=config_dir)
        
        # Debe crear config.json por defecto
        config_file = config_dir / "config.json"
        assert config_file.exists()
        
        # Valores por defecto
        assert config.get("app.name") == "cell_phone_modifier"
        assert config.get("adb.timeout") == 30
    
    def test_get_con_default(self, temp_config_dir):
        config = Config(config_dir=temp_config_dir)
        assert config.get("clave.que.no.existe", "default") == "default"
    
    def test_set_valor(self, temp_config_dir):
        config = Config(config_dir=temp_config_dir)
        config.set("app.debug", False)
        
        # Recargar para verificar persistencia
        config2 = Config(config_dir=temp_config_dir)
        assert config2.get("app.debug") is False
    
    def test_config_json_invalido(self, tmp_path):
        config_dir = tmp_path / "config"
        config_dir.mkdir()
        config_file = config_dir / "config.json"
        config_file.write_text("{json invalido}")
        
        with pytest.raises(ConfigError):
            Config(config_dir=config_dir)
    
    def test_to_dict(self, temp_config_dir):
        config = Config(config_dir=temp_config_dir)
        d = config.to_dict()
        assert isinstance(d, dict)
        assert "app" in d
        assert "adb" in d