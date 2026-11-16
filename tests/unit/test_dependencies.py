"""
Tests para el módulo de dependencias.
"""

from unittest.mock import patch

import pytest

from core.dependencies import DependencyChecker, check_dependencies
from core.errors import DependencyError


class TestDependencyChecker:
    def test_check_python(self):
        checker = DependencyChecker()
        with patch("shutil.which", return_value="/usr/bin/python"):
            valid, msg = checker.check_python()
            assert valid is True
            assert "Python" in msg
    
    def test_check_python_no_encontrado(self):
        checker = DependencyChecker()
        with patch("shutil.which", return_value=None):
            valid, msg = checker.check_python()
            assert valid is False
    
    def test_check_adb(self):
        checker = DependencyChecker()
        with patch("shutil.which", return_value="/usr/bin/adb"):
            valid, msg = checker.check_adb()
            assert valid is True
    
    def test_check_fastboot(self):
        checker = DependencyChecker()
        with patch("shutil.which", return_value="/usr/bin/fastboot"):
            valid, msg = checker.check_fastboot()
            assert valid is True
    
    def test_check_git(self):
        checker = DependencyChecker()
        with patch("shutil.which", return_value="/usr/bin/git"):
            valid, msg = checker.check_git()
            assert valid is True
    
    def test_check_all(self):
        checker = DependencyChecker()
        with patch("shutil.which", return_value="/usr/bin/mock"):
            results = checker.check_all()
            assert "python" in results
            assert "adb" in results
            assert "fastboot" in results
            assert "git" in results
    
    def test_get_missing(self):
        checker = DependencyChecker()
        with patch("shutil.which", return_value=None):
            checker.check_all()
            missing = checker.get_missing()
            assert "python" in missing
            assert "adb" in missing
    
    def test_require_exitosa(self):
        checker = DependencyChecker()
        with patch("shutil.which", return_value="/usr/bin/mock"):
            checker.check_all()
            # No debe lanzar excepción
            checker.require(["python", "adb"])
    
    def test_require_fallida(self):
        checker = DependencyChecker()
        with patch("shutil.which", return_value=None):
            checker.check_all()
            with pytest.raises(DependencyError):
                checker.require(["python"])