"""
Fixtures y configuración global para tests.
Mockea ADB y configuración para que los tests no requieran dispositivo.
"""

import json
import os
import tempfile
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest


# Mock de subprocess para ADB
class MockCompletedProcess:
    """Simula subprocess.CompletedProcess."""
    
    def __init__(self, stdout="", stderr="", returncode=0):
        self.stdout = stdout
        self.stderr = stderr
        self.returncode = returncode


@pytest.fixture
def mock_adb_output():
    """Salidas mock de comandos ADB."""
    return {
        "devices": (
            "List of devices attached\n"
            "ABC123456\tdevice product:samsung model:SM_A515M device:a51\n"
            "192.168.1.100:5555\tdevice product:pixel model:Pixel_6 device:oriole\n"
        ),
        "getprop_model": "SM-A515M",
        "getprop_brand": "samsung",
        "getprop_android": "12",
        "battery": (
            "Current Battery Service state:\n"
            "  AC powered: false\n"
            "  USB powered: true\n"
            "  status: 2\n"
            "  health: 2\n"
            "  level: 85\n"
            "  scale: 100\n"
            "  voltage: 3850\n"
            "  temperature: 280\n"
            "  technology: Li-ion\n"
        ),
        "packages": (
            "package:com.whatsapp\n"
            "package:com.telegram.messenger\n"
            "package:com.spotify.music\n"
        ),
        "df": (
            "Filesystem     1K-blocks     Used Available Use% Mounted on\n"
            "/dev/block/sda1  50000000 20000000  30000000  40% /data\n"
            "/dev/block/sdb1  10000000  5000000   5000000  50% /system\n"
        ),
    }


@pytest.fixture
def mock_subprocess(mock_adb_output):
    """Mockea subprocess.run para comandos ADB."""
    def side_effect(cmd, **kwargs):
        cmd_str = " ".join(cmd) if isinstance(cmd, list) else cmd
        
        if "devices" in cmd_str:
            return MockCompletedProcess(stdout=mock_adb_output["devices"])
        elif "getprop" in cmd_str and "model" in cmd_str:
            return MockCompletedProcess(stdout=mock_adb_output["getprop_model"])
        elif "getprop" in cmd_str and "brand" in cmd_str:
            return MockCompletedProcess(stdout=mock_adb_output["getprop_brand"])
        elif "getprop" in cmd_str and "release" in cmd_str:
            return MockCompletedProcess(stdout=mock_adb_output["getprop_android"])
        elif "dumpsys battery" in cmd_str:
            return MockCompletedProcess(stdout=mock_adb_output["battery"])
        elif "pm list packages" in cmd_str:
            return MockCompletedProcess(stdout=mock_adb_output["packages"])
        elif cmd_str.startswith("df"):
            return MockCompletedProcess(stdout=mock_adb_output["df"])
        else:
            return MockCompletedProcess(stdout="")
    
    with patch("subprocess.run", side_effect=side_effect) as mock:
        yield mock


@pytest.fixture
def temp_config_dir(tmp_path):
    """Crea un directorio temporal para configuración."""
    config_dir = tmp_path / "config"
    config_dir.mkdir()
    
    config_data = {
        "app": {"name": "test", "version": "0.1.0", "debug": True},
        "adb": {"timeout": 10, "retry_attempts": 2, "retry_delay": 1},
        "backup": {"default_path": str(tmp_path / "backups"), "compress": True},
        "logging": {"level": "DEBUG", "max_size_mb": 5, "backup_count": 2},
    }
    
    config_file = config_dir / "config.json"
    config_file.write_text(json.dumps(config_data))
    
    return config_dir


@pytest.fixture
def temp_env_file(tmp_path):
    """Crea un archivo .env temporal."""
    env_file = tmp_path / ".env"
    env_file.write_text("LOG_LEVEL=DEBUG\nADB_TIMEOUT=15\n")
    return env_file


@pytest.fixture
def sample_device_info():
    """Información de dispositivo de ejemplo."""
    return {
        "serial": "ABC123456",
        "model": "SM-A515M",
        "brand": "samsung",
        "android_version": "12",
        "sdk_version": "31",
    }


@pytest.fixture
def mock_adb_wrapper():
    """Mock de ADBWrapper."""
    adb = MagicMock()
    adb.serial = "ABC123456"
    adb.timeout = 30
    adb.get_devices.return_value = [
        {"serial": "ABC123456", "state": "device", "model": "SM-A515M"}
    ]
    adb.is_device_connected.return_value = True
    adb.get_property.return_value = "test_value"
    adb.shell.return_value = "test_output"
    adb.pull.return_value = True
    adb.push.return_value = True
    adb.install.return_value = True
    adb.uninstall.return_value = True
    adb.reboot.return_value = True
    return adb