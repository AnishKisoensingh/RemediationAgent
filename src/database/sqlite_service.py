import sqlite3
import json
import hashlib
from datetime import datetime
import logging

class SQLiteService:
    def __init__(self, db_path="remediation.db"):
        """Initialize SQLite database connection."""
        self.db_path = db_path
        self._init_db()

    def _init_db(self):
        """Initialize the database with the required tables."""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Create errors table with simplified schema
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS errors (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    error_hash TEXT UNIQUE,
                    timestamp TEXT,
                    message TEXT,
                    level TEXT,
                    remediation TEXT
                )
            """)
            
            conn.commit()
            conn.close()
        except Exception as e:
            logging.error(f"Failed to initialize SQLite database: {str(e)}")
            raise

    def _generate_hash(self, data: dict) -> str:
        """Generate a hash from the error message."""
        message = data.get("message", "")
        return hashlib.md5(message.encode()).hexdigest()

    def store_error(self, error_data: dict, remediation: dict):
        """Store error and its remediation in the database."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        error_hash = self._generate_hash(error_data)
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        try:
            cursor.execute("""
                INSERT INTO errors (error_hash, timestamp, message, level, remediation)
                VALUES (?, ?, ?, ?, ?)
            """, (
                error_hash,
                timestamp,
                error_data.get("message"),
                error_data.get("level"),
                json.dumps(remediation)
            ))
            conn.commit()
        except sqlite3.IntegrityError:
            # If error already exists, update the remediation
            cursor.execute("""
                UPDATE errors 
                SET remediation = ?, timestamp = ?
                WHERE error_hash = ?
            """, (json.dumps(remediation), timestamp, error_hash))
            conn.commit()
        finally:
            conn.close()

    def get_remediation(self, error_data: dict) -> dict:
        """Retrieve remediation for a given error."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        error_hash = self._generate_hash(error_data)
        
        cursor.execute("""
            SELECT remediation 
            FROM errors 
            WHERE error_hash = ?
        """, (error_hash,))
        
        result = cursor.fetchone()
        conn.close()
        
        if result:
            return json.loads(result[0])
        return None

    def __del__(self):
        """Close database connection when object is destroyed."""
        if hasattr(self, 'conn'):
            self.conn.close() 