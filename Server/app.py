from datetime import datetime, timezone 
from flask import Flask, jsonify, request
import database
from database import get_connection, init_database

app = Flask(__name__, static_folder="../Dashboard", static_url_path="")

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

    timestamp = datetime.now().isoformat(timespec="seconds")

    print(f"Received reading: {timestamp} - Temp: {temperature_f} F, Humidity: {humidity} %, Pressure: {pressure_hpa} hPa")

    database.insert_reading(timestamp, temperature_f, humidity, pressure_hpa)

    return jsonify({"status": "ok"}), 201

if __name__ == "__main__":
    init_database()
    app.run(host="0.0.0.0", port=5000, debug=True)