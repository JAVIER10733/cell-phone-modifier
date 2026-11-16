"""
Tests para el módulo de conexión ADB.
"""

from unittest.mock import MagicMock, patch

import pytest

from core.adb_connect import ADBConnect
from core.errors import ADBError


class TestADBConnect:
    def test_pair_exitoso(self, mock_adb_wrapper):
        mock_adb_wrapper._execute.return_value = MagicMock(
            stdout="Successfully paired to 192.168.1.100:37123",
            stderr="",
            returncode=0
        )
        
        connect = ADBConnect(adb=mock_adb_wrapper)
        exito, msg = connect.pair("192.168.1.100", 37123, "123456")
        
        assert exito is True
        assert "exitoso" in msg.lower()
    
    def test_pair_codigo_invalido(self, mock_adb_wrapper):
        connect = ADBConnect(adb=mock_adb_wrapper)
        exito, msg = connect.pair("192.168.1.100", 37123, "123")
        
        assert exito is False
        assert "6 dígitos" in msg
    
    def test_pair_ip_invalida(self, mock_adb_wrapper):
        connect = ADBConnect(adb=mock_adb_wrapper)
        exito, msg = connect.pair("999.999.999.999", 37123, "123456")
        
        assert exito is False
    
    def test_connect_exitoso(self, mock_adb_wrapper):
        mock_adb_wrapper._execute.return_value = MagicMock(
            stdout="connected to 192.168.1.100:5555",
            stderr="",
            returncode=0
        )
        
        connect = ADBConnect(adb=mock_adb_wrapper)
        exito, msg = connect.connect("192.168.1.100", 5555)
        
        assert exito is True
        assert "connected" in msg.lower()
    
    def test_connect_refused(self, mock_adb_wrapper):
        mock_adb_wrapper._execute.return_value = MagicMock(
            stdout="connection refused",
            stderr="",
            returncode=0
        )
        
        connect = ADBConnect(adb=mock_adb_wrapper)
        exito, msg = connect.connect("192.168.1.100", 5555)
        
        assert exito is False
        assert "rechazada" in msg.lower()
    
    def test_disconnect(self, mock_adb_wrapper):
        mock_adb_wrapper._execute.return_value = MagicMock(
            stdout="disconnected 192.168.1.100:5555",
            stderr="",
            returncode=0
        )
        
        connect = ADBConnect(adb=mock_adb_wrapper)
        exito, msg = connect.disconnect("192.168.1.100:5555")
        
        assert exito is True