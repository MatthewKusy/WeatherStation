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


def get_current_reading():
    with get_connection() as conn:
        row = conn.execute("""
            SELECT *
            FROM readings
            ORDER BY timestamp DESC
            LIMIT 1
        """).fetchone()

    return dict(row) if row else None

def get_today_stats(today):
    with get_connection() as conn:
        row = conn.execute("""
            SELECT
                MAX(temperature_f) AS high_temperature_f,
                MIN(temperature_f) AS low_temperature_f,
                MAX(humidity) AS high_humidity,
                MIN(humidity) AS low_humidity
            FROM readings
            WHERE date(timestamp) = ?
        """, (today,)).fetchone()

    return dict(row) if row else None

def get_recent_pressures(limit=2):
    with get_connection() as conn:
        rows = conn.execute("""
            SELECT pressure_hpa
            FROM readings
            ORDER BY timestamp DESC
            LIMIT ?
        """, (limit,)).fetchall()

    return [dict(row) for row in rows]

def get_history_since(start_time):
    with get_connection() as conn:
        rows = conn.execute("""
            SELECT *
            FROM readings
            WHERE timestamp >= ?
            ORDER BY timestamp ASC
        """, (start_time,)).fetchall()

    return [dict(row) for row in rows]