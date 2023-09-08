//Erweitertes Script um das Bild vom ESP32-Cam abzurufen und die Helligkeit, Kontrast und den internen Blitz einzustellen
//http://ESP32-CAM-IP/image
#include "WiFi.h"
#include "ESPAsyncWebServer.h"
#include "esp_camera.h"

// Wi-Fi-Zugangsdaten
const char* ssid = "yourNetworkName";
const char* password = "yourNetworkPass";

// Pin-Konfiguration für die Kamera
#define CAMERA_MODEL_AI_THINKER // Kameramodell auswählen
#include "camera_pins.h"

AsyncWebServer server(80);

int brightness = 0;  // Helligkeit (0-255)
int contrast = 0;   // Kontrast (-2-2)
bool flashOn = false; // Status der LED (Blitz)

void setup() {
  Serial.begin(115200);

  // Kamera initialisieren
  camera_config_t config;
  config.ledc_channel = LEDC_CHANNEL_0;
  config.ledc_timer = LEDC_TIMER_0;
  config.pin_d0 = Y2_GPIO_NUM;
  config.pin_d1 = Y3_GPIO_NUM;
  config.pin_d2 = Y4_GPIO_NUM;
  config.pin_d3 = Y5_GPIO_NUM;
  config.pin_d4 = Y6_GPIO_NUM;
  config.pin_d5 = Y7_GPIO_NUM;
  config.pin_d6 = Y8_GPIO_NUM;
  config.pin_d7 = Y9_GPIO_NUM;
  config.pin_xclk = XCLK_GPIO_NUM;
  config.pin_pclk = PCLK_GPIO_NUM;
  config.pin_vsync = VSYNC_GPIO_NUM;
  config.pin_href = HREF_GPIO_NUM;
  config.pin_sscb_sda = SIOD_GPIO_NUM;
  config.pin_sscb_scl = SIOC_GPIO_NUM;
  config.pin_pwdn = PWDN_GPIO_NUM;
  config.pin_reset = RESET_GPIO_NUM;
  config.xclk_freq_hz = 20000000;
  config.pixel_format = PIXFORMAT_JPEG;

  if (psramFound()) {
    config.frame_size = FRAMESIZE_UXGA;
    config.jpeg_quality = 10;
    config.fb_count = 2;
  } else {
    config.frame_size = FRAMESIZE_SVGA;
    config.jpeg_quality = 12;
    config.fb_count = 1;
  }

  // Kamera mit den Konfigurationen initialisieren
  esp_err_t err = esp_camera_init(&config);
  if (err != ESP_OK) {
    Serial.printf("Kamera-Initialisierungsfehler: %s\n", esp_err_to_name(err));
    return;
  }

  // WLAN-Verbindung herstellen
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.println("Verbindung zum WLAN...");
  }

  // Webserver-Endpunkt zum Anzeigen des Kamerabilds erstellen
  server.on("/image", HTTP_GET, [](AsyncWebServerRequest *request){
    // Hier Kamerabild mit den aktuellen Einstellungen erfassen
    camera_fb_t *fb = esp_camera_fb_get();
    if (!fb) {
      request->send(500, "text/plain", "Kamerafehler");
      return;
    }
    request->send_P(200, "image/jpeg", fb->buf, fb->len);
    esp_camera_fb_return(fb);
  });

  // Webserver-Endpunkt zum Ändern der Helligkeit
  server.on("/brightness", HTTP_POST, [](AsyncWebServerRequest *request){
    String value = request->arg("value");
    brightness = value.toInt();
    request->send(200, "text/plain", "Helligkeit geändert: " + String(brightness));
  });

  // Webserver-Endpunkt zum Ändern des Kontrasts
  server.on("/contrast", HTTP_POST, [](AsyncWebServerRequest *request){
    String value = request->arg("value");
    contrast = value.toInt();
    request->send(200, "text/plain", "Kontrast geändert: " + String(contrast));
  });

  // Webserver-Endpunkt zum Ein- und Ausschalten der LED (Blitz)
  server.on("/flash", HTTP_POST, [](AsyncWebServerRequest *request){
    String value = request->arg("value");
    if (value == "on") {
      flashOn = true;
    } else if (value == "off") {
      flashOn = false;
    }
    request->send(200, "text/plain", "LED (Blitz) geändert: " + String(flashOn ? "EIN" : "AUS"));
  });

  server.begin();
}

void loop() {

