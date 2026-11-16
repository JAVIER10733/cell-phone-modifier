"""
Tests para el módulo de validadores.
"""

import pytest

from core.validators import (
    validate_host_port,
    validate_ip,
    validate_path,
    validate_port,
    validate_serial,
    validate_serial_or_ip,
)


class TestValidateSerial:
    def test_serial_valido(self):
        valid, msg = validate_serial("ABC123456")
        assert valid is True
        assert "válido" in msg.lower()
    
    def test_serial_con_guiones(self):
        valid, msg = validate_serial("device-01_test")
        assert valid is True
    
    def test_serial_ip_puerto(self):
        valid, msg = validate_serial("192.168.1.100:5555")
        assert valid is True
    
    def test_serial_vacio(self):
        valid, msg = validate_serial("")
        assert valid is False
    
    def test_serial_none(self):
        valid, msg = validate_serial(None)
        assert valid is False
    
    def test_serial_muy_corto(self):
        valid, msg = validate_serial("AB")
        assert valid is False
    
    def test_serial_caracteres_invalidos(self):
        valid, msg = validate_serial("device@#$%")
        assert valid is False


class TestValidateIP:
    def test_ip_valida(self):
        valid, msg = validate_ip("192.168.1.100")
        assert valid is True
    
    def test_ip_localhost(self):
        valid, msg = validate_ip("127.0.0.1")
        assert valid is True
    
    def test_ip_invalida_formato(self):
        valid, msg = validate_ip("999.999.999.999")
        assert valid is False
    
    def test_ip_fuera_rango(self):
        valid, msg = validate_ip("256.1.1.1")
        assert valid is False
    
    def test_ip_vacia(self):
        valid, msg = validate_ip("")
        assert valid is False
    
    def test_ip_no_string(self):
        valid, msg = validate_ip(12345)
        assert valid is False


class TestValidatePort:
    def test_puerto_valido(self):
        valid, msg = validate_port(5555)
        assert valid is True
    
    def test_puerto_minimo(self):
        valid, msg = validate_port(1)
        assert valid is True
    
    def test_puerto_maximo(self):
        valid, msg = validate_port(65535)
        assert valid is True
    
    def test_puerto_cero(self):
        valid, msg = validate_port(0)
        assert valid is False
    
    def test_puerto_negativo(self):
        valid, msg = validate_port(-1)
        assert valid is False
    
    def test_puerto_no_entero(self):
        valid, msg = validate_port("5555")
        assert valid is False


class TestValidatePath:
    def test_ruta_valida_existente(self, tmp_path):
        valid, msg, path = validate_path(str(tmp_path), must_exist=True)
        assert valid is True
        assert path is not None
    
    def test_ruta_no_existente(self):
        valid, msg, path = validate_path("/ruta/que/no/existe", must_exist=True)
        assert valid is False
    
    def test_ruta_creable(self, tmp_path):
        new_path = str(tmp_path / "nueva" / "carpeta")
        valid, msg, path = validate_path(new_path, create=True)
        assert valid is True
        assert path.exists()
    
    def test_ruta_vacia(self):
        valid, msg, path = validate_path("")
        assert valid is False


class TestValidateHostPort:
    def test_host_port_valido(self):
        valid, msg = validate_host_port("192.168.1.100", 5555)
        assert valid is True
    
    def test_host_invalido(self):
        valid, msg = validate_host_port("999.999.999.999", 5555)
        assert valid is False
    
    def test_port_invalido(self):
        valid, msg = validate_host_port("192.168.1.100", 0)
        assert valid is False


class TestValidateSerialOrIP:
    def test_serial(self):
        valid, tipo, msg = validate_serial_or_ip("ABC123456")
        assert valid is True
        assert tipo == "serial"
    
    def test_ip_puerto(self):
        valid, tipo, msg = validate_serial_or_ip("192.168.1.100:5555")
        assert valid is True
        assert tipo == "ip_port"
    
    def test_invalido(self):
        valid, tipo, msg = validate_serial_or_ip("")
        assert valid is False