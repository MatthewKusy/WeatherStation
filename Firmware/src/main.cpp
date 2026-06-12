#include <Arduino.h>
#include <Wire.h>
#include <Adafruit_BME280.h>
#include <U8g2lib.h>
#include <WiFi.h>
#include <HTTPClient.h>
#include "secrets.h"

void readSensor();
void updateDisplay();
void sendToServer();

Adafruit_BME280 bme;

U8G2_SH1106_128X64_NONAME_F_HW_I2C oled(
    U8G2_R0,
    U8X8_PIN_NONE);

const unsigned long READ_INTERVAL_MS = 5UL * 60UL * 1000UL; // 5 minutes
unsigned long lastReadTime = 0;

float temperatureF = 0;
float humidity = 0;
float pressureHPa = 0;

void setup()
{
  Serial.begin(9600);
  Serial.println("Booting...");

  WiFi.begin(WIFI_SSID, WIFI_PASSWORD);

  while (WiFi.status() != WL_CONNECTED)
  {
    delay(500);
    Serial.print(".");
  }

  Serial.println();
  Serial.println("WiFi connected");
  Serial.print("ESP32 IP address: ");
  Serial.println(WiFi.localIP());

  Wire.begin();
  oled.begin();
  oled.clearBuffer();
  oled.setFont(u8g2_font_6x12_tf);
  oled.drawStr(0, 12, "Starting...");
  oled.sendBuffer();

  if (!bme.begin(0x76))
  { // Try 0x77 if 0x76 does not work
    Serial.println("Could not find BME280 sensor!");
    oled.clearBuffer();
    oled.drawStr(0, 12, "BME280 not found");
    oled.sendBuffer();

    while (true)
    {
      delay(1000);
    }
  }

  Serial.println("BME280 ready");

  readSensor();
  updateDisplay(); // Read once immediately at startup
  sendToServer();
  lastReadTime = millis();
}

void loop()
{
  unsigned long now = millis();
  // put your main code here, to run repeatedly:
  if (now - lastReadTime >= READ_INTERVAL_MS)
  {
    readSensor();
    updateDisplay();
    lastReadTime = now;
    sendToServer();
  }
}

void readSensor()
{
  float temperatureC = bme.readTemperature();
  humidity = bme.readHumidity();
  pressureHPa = bme.readPressure() / 100.0F;

  temperatureF = temperatureC * 9.0 / 5.0 + 32.0;

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

void updateDisplay()
{
  oled.clearBuffer();

  oled.setFont(u8g2_font_6x12_tf);

  oled.drawStr(0, 12, "Weather Station");

  oled.setCursor(0, 28);
  oled.print("Temperature: ");
  oled.print(temperatureF, 2);
  oled.print(" F");

  oled.setCursor(0, 42);
  oled.print("Humidity: ");
  oled.print(humidity, 2);
  oled.print(" %");

  oled.setCursor(0, 56);
  oled.print("Pressure: ");
  oled.print(pressureHPa, 1);
  oled.print(" hPa");

  oled.sendBuffer();
}

void sendToServer()
{
  if (WiFi.status() != WL_CONNECTED)
  {
    Serial.println("WiFi not connected");
    return;
  }

  HTTPClient http;
  http.begin(SERVER_URL);
  http.addHeader("Content-Type", "application/json");

  String json = "{";
  json += "\"temperatureF\":";
  json += String(temperatureF, 2);
  json += ",";
  json += "\"humidity\":";
  json += String(humidity, 2);
  json += ",";
  json += "\"pressureHpa\":";
  json += String(pressureHPa, 1);
  json += "}";

  int responseCode = http.POST(json);

  Serial.print("Server response: ");
  Serial.println(responseCode);

  http.end();
}