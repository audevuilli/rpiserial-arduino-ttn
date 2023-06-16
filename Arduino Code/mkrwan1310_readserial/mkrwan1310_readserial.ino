/* LoRa Send Message to TTN console */
#include <MKRWAN.h>
#include <ArduinoLowPower.h>
#include "arduino_secrets.h"
#include <vector>

LoRaModem modem;

// Set the appEui and appKey from arduino_secrets.h
String appEui = SECRET_APP_EUI;
String appKey = SECRET_APP_KEY;

#define SERIAL_BAUD_RATE 115200

// Create a vector to store the received messages.
std::vector<String> receivedMessages;

void setup() {

  Serial.begin(SERIAL_BAUD_RATE);
  
  while (!Serial);
    // Change this to regional band (eg. US915, AS923, ...)
    if (!modem.begin(EU868)) {
      Serial.print("Failed to start module");
      while (1) {}
  };

  int connected = modem.joinOTAA(appEui, appKey);
  if (!connected) {
    Serial.print("Something went wrong; are you indoor? Move near a window and retry");
    while (1) {}
  }
  
  delay(100); 
  Serial.println("  - Connected to TTN ");

  // Set poll interval to 60 secs.
  modem.minPollInterval(60);
}

void loop() {

  // Read data from serial port
  if (Serial.available() > 0) {
    // Get incoming byte:
    String msg = Serial.readStringUntil('\n');
    // Read from serial 
    for (unsigned int i = 0; i < msg.length(); i++) {
      Serial.print(msg[i] >> 4, HEX);
      Serial.print(msg[i] & 0xF, HEX);
      Serial.print(" ");
    }
    // Add the recieved message to the msgs array
    receivedMessages.push_back(msg);

    // Loop through the msgs array and send the data to TTN
    for (const auto& msg: receivedMessages){ 
      sendData(msg);
    }
    
    // Clear the receivedMessages vector - make it empty for next msgs.
    receivedMessages.clear();
  }
}

void sendData(const String& msg){
  
  // Send the sensor values
  int err;
  modem.beginPacket();
  modem.print(msg);
  err = modem.endPacket(true);

  if (err > 0) {
    Serial.println("Message sent correctly!");
  } else {
    Serial.println("Error sending message :(");
  }

  delay(1000);
}