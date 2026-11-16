"""
Test de flujo de backup (integración con mocks).
"""

from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from core.modules.backup import BackupModule
from core.modules.restore import RestoreModule


class TestBackupFlow:
    def test_backup_apk(self, tmp_path, mock_adb_wrapper):
        # Mockear pull para simular copia de APK
        mock_adb_wrapper.shell.return_value = "package:/data/app/com.test-1/base.apk"
        mock_adb_wrapper.pull.return_value = True
        
        module = BackupModule(adb=mock_adb_wrapper)
        
        # Override del directorio de backup
        with patch.object(module, "_get_backup_dir", return_value=tmp_path / "backups"):
            path = module.backup_apk("com.test")
            
            assert path is not None
            assert "com.test" in path
            mock_adb_wrapper.pull.assert_called_once()
    
    def test_restore_apk(self, tmp_path, mock_adb_wrapper):
        # Crear APK falso
        apk_file = tmp_path / "test.apk"
        apk_file.write_text("fake apk content")
        
        mock_adb_wrapper.install.return_value = True
        
        module = RestoreModule(adb=mock_adb_wrapper)
        result = module.restore_apk(str(apk_file))
        
        assert result is True
        mock_adb_wrapper.install.assert_called_once()
    
    def test_restore_apk_no_existe(self, mock_adb_wrapper):
        module = RestoreModule(adb=mock_adb_wrapper)
        
        with pytest.raises(Exception):
            module.restore_apk("/ruta/no/existe.apk")
    
    def test_backup_all_apks(self, tmp_path, mock_adb_wrapper):
        mock_adb_wrapper._execute.return_value = MagicMock(
            stdout="package:com.whatsapp\npackage:com.telegram\n",
            stderr="",
            returncode=0
        )
        mock_adb_wrapper.shell.return_value = "package:/data/app/com.test-1/base.apk"
        mock_adb_wrapper.pull.return_value = True
        
        module = BackupModule(adb=mock_adb_wrapper)
        
        with patch.object(module, "_get_backup_dir", return_value=tmp_path / "backups"):
            paths = module.backup_all_apks()
            
            assert len(paths) == 2