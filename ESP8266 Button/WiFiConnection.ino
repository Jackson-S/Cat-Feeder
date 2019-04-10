void connectToNetwork() {
  // Change default network page from 192.168.4.1
  // to 192.168.1.1
  wifiManager.setAPStaticIPConfig(PORTAL_IP, PORTAL_IP, SUBNET_MASK);

  // Attempt to connect to access point previously
  // connected to, on failing that create a network
  // to allow further network setup.
  Serial.println("Initiating Network Connection");
  wifiManager.autoConnect(AP_NAME);
}

void forgetNetworkSettings() {
  Serial.println("Forgetting Network Settings!");
  wifiManager.resetSettings();
  // Terminates running
  ESP.restart();
}

void sleepWiFiChipset() {
  Serial.println("Sleeping WiFi Chipset");
  WiFi.mode(WIFI_OFF);
  WiFi.forceSleepBegin();
}
