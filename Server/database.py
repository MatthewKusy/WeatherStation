import sqlite3
from pathlib import Path

DB_PATH = Path("weather.db")

def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_database():
    with get_connection() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS readings (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                temperature_f REAL NOT NULL,
                humidity REAL NOT NULL,
                pressure_hpa REAL NOT NULL
            )
        """)

def insert_reading(timestamp, temperature_f, humidity, pressure_hpa):
    with get_connection() as conn:
        conn.execute("""
            INSERT INTO readings (
                timestamp,
                temperature_f,
                humidity,
                pressure_hpa
            )
            VALUES (?, ?, ?, ?)
        """, (
            timestamp,
            temperature_f,
            humidity,
            pressure_hpa
        ))