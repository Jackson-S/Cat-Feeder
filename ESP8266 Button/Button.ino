Switch button = Switch(BUTTON_PIN);

void checkForPush() {
  static bool doubleClicked = false;
  // Check the button's state over time.
  button.poll();

  if (button.singleClick()) {
    doubleClicked = false;
    Serial.println("Single click.");
    registerFeed();
  } else if (button.doubleClick()) {
    doubleClicked = true;
    Serial.println("Double clicked.");
  } else if (button.longPress() && doubleClicked) {
    doubleClicked = false;
    Serial.println("Long press after double click.");
    forgetNetworkSettings();
  }
}
