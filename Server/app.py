from datetime import datetime, timezone 
import sqlite3
from flask import Flask, jsonify, request
from pathlib import Path

app = Flask(__name__, static_folder="../Dashboard", static_url_path="")

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

@app.get("/")
def index():
    return app.send_static_file("index.html")

@app.post("/api/readings")
def add_reading():
    data = request.get_json()

    if data is None:
        return jsonify({"error": "JSON body is required"}), 400

    try:
        temperature_f = float(data["temperatureF"])
        humidity = float(data["humidity"])
        pressure_hpa = float(data["pressureHpa"])
    except KeyError as e:
        return jsonify({"error": f"Missing field: {e.args[0]}"}), 400
    except ValueError:
        return jsonify({"error": "Temperature, humidity, and pressure must be numbers"}), 400

    timestamp = datetime.now(timezone.utc).isoformat(timespec="seconds")

    with get_connection() as conn:
        conn.execute("""
            INSERT INTO readings (timestamp, temperature_f, humidity, pressure_hpa)
            VALUES (?, ?, ?, ?)
        """, (timestamp, temperature_f, humidity, pressure_hpa))

    return jsonify({"status": "ok"}), 201

if __name__ == "__main__":
    init_database()
    app.run(host="0.0.0.0", port=5000, debug=True)