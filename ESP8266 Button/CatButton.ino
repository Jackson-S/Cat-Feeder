/*
   Cat feeder button app. Should work with ESP-8266 based
   devices. May work with other devices with slight modifications
   but I don't have anything to test it on.

   Button is connected to D3 by default.

   A single push will update the web app, to reset
   WiFi double push then hold and connect to the
   "Cat Button Setup" netowrk. Go to 192.168.1.1
   and enter WiFi details, these will be saved for all
   subsequent boots.
*/

#include <WiFiManager.h>
#include <ESP8266HTTPClient.h>
#include <avdweb_Switch.h>

// Replace with IP Address or URL of the site hosting
// the web app.
const extern String SITE_ADDRESS = "192.168.1.1";
const extern String SITE_URI = "/record_feed";
const extern uint16_t SITE_PORT = 45000;

const extern IPAddress PORTAL_IP = IPAddress(192, 168, 1, 1);
const extern IPAddress SUBNET_MASK = IPAddress(255, 255, 255, 0);
const extern char AP_NAME[] = "Cat Button Setup";

// The pin the button is connected to by default.
const extern byte BUTTON_PIN = D3;

// Initialize WiFiManager library.
WiFiManager wifiManager;

void setup() {
  // Same serial rate as used by init code when starting device
  Serial.begin(74880);
  connectToNetwork();
}

void loop() {
  checkForPush();
}
