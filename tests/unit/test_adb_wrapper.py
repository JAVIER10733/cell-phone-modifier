"""
Tests para el wrapper de ADB.
"""

from unittest.mock import MagicMock, patch

import pytest

from core.adb_wrapper import ADBWrapper
from core.errors import ADBError, DeviceError, TimeoutError


class TestADBWrapper:
    def test_build_command_sin_serial(self):
        adb = ADBWrapper()
        cmd = adb._build_command(["devices"])
        assert cmd == ["adb", "devices"]
    
    def test_build_command_con_serial(self):
        adb = ADBWrapper(serial="ABC123456")
        cmd = adb._build_command(["devices"])
        assert cmd == ["adb", "-s", "ABC123456", "devices"]
    
    def test_get_devices(self, mock_subprocess, mock_adb_output):
        adb = ADBWrapper()
        devices = adb.get_devices()
        
        assert len(devices) == 2
        assert devices[0]["serial"] == "ABC123456"
        assert devices[0]["state"] == "device"
        assert devices[1]["serial"] == "192.168.1.100:5555"
    
    def test_is_device_connected(self, mock_subprocess):
        adb = ADBWrapper(serial="ABC123456")
        assert adb.is_device_connected() is True
    
    def test_is_device_not_connected(self, mock_subprocess):
        adb = ADBWrapper(serial="SERIAL_INEXISTENTE")
        assert adb.is_device_connected() is False
    
    def test_get_property(self, mock_subprocess):
        adb = ADBWrapper()
        result = adb.get_property("ro.product.model")
        assert result == "SM-A515M"
    
    def test_shell(self, mock_subprocess):
        adb = ADBWrapper()
        result = adb.shell("echo test")
        assert result == "test_output"
    
    def test_pull(self, mock_subprocess):
        adb = ADBWrapper()
        assert adb.pull("/sdcard/test.txt", "/tmp/test.txt") is True
    
    def test_push(self, mock_subprocess, tmp_path):
        # Crear archivo local
        local_file = tmp_path / "test.txt"
        local_file.write_text("contenido")
        
        adb = ADBWrapper()
        assert adb.push(str(local_file), "/sdcard/test.txt") is True
    
    def test_push_archivo_no_existe(self):
        adb = ADBWrapper()
        with pytest.raises(ADBError):
            adb.push("/ruta/no/existe.txt", "/sdcard/test.txt")
    
    def test_set_serial_valido(self):
        adb = ADBWrapper()
        adb.set_serial("ABC123456")
        assert adb.serial == "ABC123456"
    
    def test_set_serial_invalido(self):
        adb = ADBWrapper()
        with pytest.raises(ADBError):
            adb.set_serial("")
    
    def test_timeout(self, mock_subprocess):
        mock_subprocess.side_effect = __import__("subprocess").TimeoutExpired("adb", 30)
        adb = ADBWrapper()
        with pytest.raises(TimeoutError):
            adb.get_devices()