#include <WiFi.h>
#include <HTTPClient.h>
#include <ArduinoJson.h>
#include <DHT.h>

// WiFi credentials
const char* ssid = "TWÓJ_SSID";
const char* password = "TWOJE_HASŁO";

// Cloud Run URL
const char* serverUrl = "https://iot-rest-562390583242.us-central1.run.app/";

// DHT11 configuration
#define DHTPIN 4       // Pin do którego podłączony jest DHT11
#define DHTTYPE DHT11  // Typ czujnika (DHT11)
DHT dht(DHTPIN, DHTTYPE);

// Delay between measurements (5 seconds)
const int delayTime = 5000;

void setup() {
  Serial.begin(115200);
  
  // Initialize DHT sensor
  dht.begin();
  Serial.println("DHT11 initialized");
  
  // Connect to WiFi
  WiFi.begin(ssid, password);
  Serial.println("Connecting to WiFi");
  
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  
  Serial.println("");
  Serial.println("WiFi connected");
  Serial.println("IP address: ");
  Serial.println(WiFi.localIP());
}

float getTemperature() {
  // Read temperature from DHT11
  float temp = dht.readTemperature();
  
  // Check if reading was successful
  if (isnan(temp)) {
    Serial.println("Failed to read from DHT11 sensor!");
    return -999; // Error value
  }
  
  return temp;
}

void sendTemperature(float temp) {
  // Don't send error readings
  if (temp == -999) return;
  
  if (WiFi.status() == WL_CONNECTED) {
    HTTPClient http;
    
    // Initialize HTTP client
    http.begin(serverUrl);
    http.addHeader("Content-Type", "application/json");
    
    // Create JSON document
    StaticJsonDocument<200> doc;
    
    // Formatowanie temperatury do 2 miejsc po przecinku
    char tempStr[10];
    dtostrf(temp, 1, 2, tempStr);  // Konwertuje float na string z 2 miejscami po przecinku
    doc["temperatura"] = atof(tempStr);  // Konwertuje string z powrotem na float
    
    // Serialize JSON
    String jsonString;
    serializeJson(doc, jsonString);
    
    // Print JSON for debugging
    Serial.print("Sending JSON: ");
    Serial.println(jsonString);
    
    // Send POST request
    int httpResponseCode = http.POST(jsonString);
    
    if (httpResponseCode > 0) {
      String response = http.getString();
      Serial.println("HTTP Response code: " + String(httpResponseCode));
      Serial.println("Response: " + response);
    } else {
      Serial.println("Error on sending POST: " + String(httpResponseCode));
    }
    
    http.end();
  } else {
    Serial.println("WiFi Disconnected");
    // Próba ponownego połączenia
    WiFi.begin(ssid, password);
  }
}

void loop() {
  float temperature = getTemperature();
  
  if (temperature != -999) {
    Serial.print("Temperature: ");
    Serial.print(temperature, 2);  // 2 miejsca po przecinku
    Serial.println("°C");
    
    sendTemperature(temperature);
  }
  
  delay(delayTime);
}