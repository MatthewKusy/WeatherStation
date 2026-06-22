from datetime import datetime, timedelta
import math
import random

import database


def generate_temperature(timestamp):
    hour = timestamp.hour + timestamp.minute / 60

    daily_cycle = math.sin((hour - 6) * math.pi / 12)

    base_temp = 72
    daily_swing = 12
    noise = random.uniform(-1.5, 1.5)

    return round(base_temp + daily_swing * daily_cycle + noise, 1)


def generate_humidity(temperature_f):
    base_humidity = 55

    temp_effect = (72 - temperature_f) * 0.8
    noise = random.uniform(-4, 4)

    humidity = base_humidity + temp_effect + noise

    humidity = max(20, min(95, humidity))

    return round(humidity, 1)


def generate_pressure(timestamp):
    day_number = timestamp.timetuple().tm_yday

    weather_pattern = math.sin(day_number * math.pi / 5)

    base_pressure = 1013
    swing = 0.18
    noise = random.uniform(-0.03, 0.03)

    return round(base_pressure + swing * weather_pattern + noise, 2)


def seed_database(days=30, interval_minutes=5):
    database.init_database()

    start_time = datetime.now() - timedelta(days=days)

    total_readings = int(
        (days * 24 * 60) / interval_minutes
    )

    for i in range(total_readings):

        timestamp = start_time + timedelta(
            minutes=i * interval_minutes
        )

        temperature_f = generate_temperature(timestamp)

        humidity = generate_humidity(
            temperature_f
        )

        pressure_inhg = generate_pressure(
            timestamp
        )

        database.insert_reading(
            timestamp.isoformat(),
            temperature_f,
            humidity,
            pressure_inhg
        )

    print(
        f"Inserted {total_readings} fake readings."
    )


if __name__ == "__main__":
    seed_database()