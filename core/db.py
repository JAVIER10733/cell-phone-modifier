"""
Base de datos SQLite para cell_phone_modifier.
Almacena historial de acciones, configuraciones y metadatos.
"""

import sqlite3
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from core.errors import StorageError
from core.logger import logger
from core.platform_utils import get_termux_paths, is_termux


class Database:
    """Base de datos SQLite local."""
    
    def __init__(self, db_path: Optional[Path] = None) -> None:
        if db_path:
            self.db_path = db_path
        elif is_termux():
            paths = get_termux_paths()
            self.db_path = paths["home"] / "cell_phone_modifier" / "data" / "app.db"
        else:
            self.db_path = Path(__file__).parent.parent / "data" / "app.db"
        
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self.conn: Optional[sqlite3.Connection] = None
    
    def initialize(self) -> None:
        """Inicializa la base de datos y crea tablas."""
        try:
            self.conn = sqlite3.connect(str(self.db_path))
            self.conn.row_factory = sqlite3.Row
            self._create_tables()
            logger.info(f"Base de datos inicializada en: {self.db_path}")
        except sqlite3.Error as e:
            raise StorageError(f"Error inicializando base de datos: {e}")
    
    def _create_tables(self) -> None:
        """Crea las tablas necesarias."""
        cursor = self.conn.cursor()
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS actions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                module TEXT NOT NULL,
                action TEXT NOT NULL,
                args TEXT,
                result TEXT,
                success INTEGER DEFAULT 1,
                error TEXT
            )
        """)
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS devices (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                serial TEXT UNIQUE NOT NULL,
                model TEXT,
                brand TEXT,
                android_version TEXT,
                first_seen TEXT NOT NULL,
                last_seen TEXT NOT NULL
            )
        """)
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS backups (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                type TEXT NOT NULL,
                path TEXT NOT NULL,
                package TEXT,
                device_serial TEXT,
                size_bytes INTEGER,
                checksum TEXT
            )
        """)
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS settings (
                key TEXT PRIMARY KEY,
                value TEXT NOT NULL,
                updated_at TEXT NOT NULL
            )
        """)
        
        self.conn.commit()
    
    def log_action(
        self,
        module: str,
        args: Optional[Dict[str, Any]] = None,
        result: Any = None,
        success: bool = True,
        error: Optional[str] = None
    ) -> int:
        """
        Registra una acción en el historial.
        
        Args:
            module: Nombre del módulo
            args: Argumentos de la acción
            result: Resultado de la acción
            success: Si fue exitosa
            error: Mensaje de error si falló
        
        Returns:
            int: ID de la acción registrada
        """
        if not self.conn:
            return -1
        
        import json
        
        cursor = self.conn.cursor()
        cursor.execute(
            """
            INSERT INTO actions (timestamp, module, action, args, result, success, error)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (
                datetime.now().isoformat(),
                module,
                module,
                json.dumps(args) if args else None,
                json.dumps(result) if result else None,
                1 if success else 0,
                error
            )
        )
        self.conn.commit()
        return cursor.lastrowid
    
    def get_actions(
        self,
        module: Optional[str] = None,
        limit: int = 100
    ) -> List[Dict[str, Any]]:
        """
        Obtiene acciones del historial.
        
        Args:
            module: Filtrar por módulo
            limit: Máximo de registros
        
        Returns:
            List[Dict[str, Any]]: Lista de acciones
        """
        if not self.conn:
            return []
        
        cursor = self.conn.cursor()
        
        if module:
            cursor.execute(
                "SELECT * FROM actions WHERE module = ? ORDER BY timestamp DESC LIMIT ?",
                (module, limit)
            )
        else:
            cursor.execute(
                "SELECT * FROM actions ORDER BY timestamp DESC LIMIT ?",
                (limit,)
            )
        
        return [dict(row) for row in cursor.fetchall()]
    
    def register_device(
        self,
        serial: str,
        model: Optional[str] = None,
        brand: Optional[str] = None,
        android_version: Optional[str] = None
    ) -> None:
        """Registra o actualiza un dispositivo."""
        if not self.conn:
            return
        
        now = datetime.now().isoformat()
        cursor = self.conn.cursor()
        
        cursor.execute(
            """
            INSERT INTO devices (serial, model, brand, android_version, first_seen, last_seen)
            VALUES (?, ?, ?, ?, ?, ?)
            ON CONFLICT(serial) DO UPDATE SET
                model = COALESCE(excluded.model, devices.model),
                brand = COALESCE(excluded.brand, devices.brand),
                android_version = COALESCE(excluded.android_version, devices.android_version),
                last_seen = excluded.last_seen
            """,
            (serial, model, brand, android_version, now, now)
        )
        self.conn.commit()
    
    def get_devices(self) -> List[Dict[str, Any]]:
        """Obtiene todos los dispositivos registrados."""
        if not self.conn:
            return []
        
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM devices ORDER BY last_seen DESC")
        return [dict(row) for row in cursor.fetchall()]
    
    def register_backup(
        self,
        backup_type: str,
        path: str,
        package: Optional[str] = None,
        device_serial: Optional[str] = None,
        size_bytes: Optional[int] = None,
        checksum: Optional[str] = None
    ) -> int:
        """Registra un backup."""
        if not self.conn:
            return -1
        
        cursor = self.conn.cursor()
        cursor.execute(
            """
            INSERT INTO backups (timestamp, type, path, package, device_serial, size_bytes, checksum)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (
                datetime.now().isoformat(),
                backup_type,
                path,
                package,
                device_serial,
                size_bytes,
                checksum
            )
        )
        self.conn.commit()
        return cursor.lastrowid
    
    def get_backups(self, limit: int = 50) -> List[Dict[str, Any]]:
        """Obtiene backups registrados."""
        if not self.conn:
            return []
        
        cursor = self.conn.cursor()
        cursor.execute(
            "SELECT * FROM backups ORDER BY timestamp DESC LIMIT ?",
            (limit,)
        )
        return [dict(row) for row in cursor.fetchall()]
    
    def get_setting(self, key: str, default: Optional[str] = None) -> Optional[str]:
        """Obtiene un valor de configuración."""
        if not self.conn:
            return default
        
        cursor = self.conn.cursor()
        cursor.execute("SELECT value FROM settings WHERE key = ?", (key,))
        row = cursor.fetchone()
        return row["value"] if row else default
    
    def set_setting(self, key: str, value: str) -> None:
        """Establece un valor de configuración."""
        if not self.conn:
            return
        
        cursor = self.conn.cursor()
        cursor.execute(
            """
            INSERT INTO settings (key, value, updated_at)
            VALUES (?, ?, ?)
            ON CONFLICT(key) DO UPDATE SET
                value = excluded.value,
                updated_at = excluded.updated_at
            """,
            (key, value, datetime.now().isoformat())
        )
        self.conn.commit()
    
    def close(self) -> None:
        """Cierra la conexión."""
        if self.conn:
            self.conn.close()
            self.conn = None
            logger.debug("Base de datos cerrada")