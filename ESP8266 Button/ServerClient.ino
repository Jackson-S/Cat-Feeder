bool registerFeed() {
  HTTPClient client;

  bool result;

  // Configure server to connect to.
  client.begin(SITE_ADDRESS, SITE_PORT, SITE_URI);

  // Post an empty request to the server
  int returnCode = client.POST("");

  // Check for a found status (302) as this is what
  // the server will respond with.
  if (returnCode != HTTP_CODE_FOUND && returnCode != HTTP_CODE_OK) {
    Serial.print("Netowrk load failed with code: ");
    Serial.println(returnCode);
    result = false;
  } else {
    Serial.println("Network load completed");
    result = true;
  }

  // Close the connection.
  client.end();
  
  return result;
}
