from datetime import datetime 
from flask import Flask, jsonify, request

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

    print(f"Received reading at {timestamp}: {temperature_f}°F, {humidity}%, {pressure_hpa} hPa")

    return jsonify({"status": "ok"}), 201

if __name__ == "__main__":
    app.run(debug=True)