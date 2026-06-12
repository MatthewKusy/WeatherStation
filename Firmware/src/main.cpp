#include <Arduino.h>
#include <Wire.h>
#include <Adafruit_BME280.h>

void readSensor();

Adafruit_BME280 bme;

const unsigned long READ_INTERVAL_MS = 5UL * 60UL * 1000UL; // 5 minutes
unsigned long lastReadTime = 0;

void setup() {
  Serial.begin(9600);
  Serial.println("Booting...");
  Wire.begin();

  if (!bme.begin(0x76)) {   // Try 0x77 if 0x76 does not work
    Serial.println("Could not find BME280 sensor!");
    while (true) {
      delay(1000);  
    }
  }
  Serial.println("BME280 ready");

  readSensor();             // Read once immediately at startup
  lastReadTime = millis();
}

void loop() {
  unsigned long now = millis();
  // put your main code here, to run repeatedly:
  if (now - lastReadTime >= READ_INTERVAL_MS) {
    readSensor();
    lastReadTime = now;
  }
}

void readSensor() {
  float temperatureC = bme.readTemperature();
  float humidity = bme.readHumidity();
  float pressureHPa = bme.readPressure() / 100.0F;

  float temperatureF = temperatureC * 9.0 / 5.0 + 32.0;

  Serial.print("Temperature: ");
  Serial.print(temperatureF);
  Serial.println(" °F");

  Serial.print("Humidity: ");
  Serial.print(humidity);
  Serial.println(" %");

  Serial.print("Pressure: ");
  Serial.print(pressureHPa);
  Serial.println(" hPa");

  Serial.println();
}
