"""
Tests para el wrapper de Fastboot.
"""

from unittest.mock import MagicMock, patch

import pytest

from core.errors import FastbootError
from core.fastboot_wrapper import FastbootWrapper


class TestFastbootWrapper:
    def test_build_command_sin_serial(self):
        fb = FastbootWrapper()
        cmd = fb._build_command(["devices"])
        assert cmd == ["fastboot", "devices"]
    
    def test_build_command_con_serial(self):
        fb = FastbootWrapper(serial="ABC123456")
        cmd = fb._build_command(["devices"])
        assert cmd == ["fastboot", "-s", "ABC123456", "devices"]
    
    def test_get_devices(self):
        mock_result = MagicMock(
            stdout="ABC123456\tfastboot\nXYZ789\tfastboot\n",
            stderr="",
            returncode=0
        )
        
        with patch("subprocess.run", return_value=mock_result):
            fb = FastbootWrapper()
            devices = fb.get_devices()
            
            assert len(devices) == 2
            assert devices[0] == "ABC123456"
            assert devices[1] == "XYZ789"
    
    def test_get_var(self):
        mock_result = MagicMock(
            stdout="",
            stderr="product: SM-A515M\n",
            returncode=0
        )
        
        with patch("subprocess.run", return_value=mock_result):
            fb = FastbootWrapper()
            value = fb.get_var("product")
            assert value == "SM-A515M"
    
    def test_reboot(self):
        mock_result = MagicMock(returncode=0)
        
        with patch("subprocess.run", return_value=mock_result):
            fb = FastbootWrapper()
            assert fb.reboot() is True
    
    def test_flash(self):
        mock_result = MagicMock(returncode=0)
        
        with patch("subprocess.run", return_value=mock_result):
            fb = FastbootWrapper()
            assert fb.flash("boot", "/tmp/boot.img") is True
    
    def test_erase(self):
        mock_result = MagicMock(returncode=0)
        
        with patch("subprocess.run", return_value=mock_result):
            fb = FastbootWrapper()
            assert fb.erase("cache") is True
    
    def test_fastboot_no_encontrado(self):
        with patch("subprocess.run", side_effect=FileNotFoundError):
            fb = FastbootWrapper()
            with pytest.raises(FastbootError):
                fb.get_devices()