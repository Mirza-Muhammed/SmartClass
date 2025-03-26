#include <SPI.h>
#include <MFRC522.h>
#include <WiFi.h>
#include <HTTPClient.h>

const char* ssid = "Hasheer Manzil_EXT";
const char* password = "haneesh@123";

#define RST_PIN  4
#define SS_PIN   21

MFRC522 mfrc522(SS_PIN, RST_PIN);

const String registerEndpoint = "http://192.168.1.103:5000/register_nfc";
const String scanEndpoint = "http://192.168.1.103:5000/scan_nfc";

bool isRegistrationMode = false;
bool isRunning = true;
String role = "student";

void setup() {
  Serial.begin(115200);
  SPI.begin();
  mfrc522.PCD_Init();
  
  WiFi.begin(ssid, password);
  Serial.print("Connecting to WiFi...");
  
  int attempts = 0;
  while (WiFi.status() != WL_CONNECTED && attempts < 20) {  
    delay(1000);
    Serial.print(".");
    attempts++;
  }

  if (WiFi.status() != WL_CONNECTED) {
    Serial.println("\nFailed to connect to WiFi. Please check your network and restart the device.");
    while (true);
}

  Serial.println("\nConnected to WiFi!");
  Serial.println("\nSystem ready. Type 'register' to enter registration mode, 'scan' to enter scanning mode, or 'exit' to stop.");
}

void reconnectWiFi() {
  Serial.println("WiFi Disconnected! Reconnecting...");
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.print(".");
  }
  Serial.println("\nReconnected to WiFi!");
}



void loop() {
  if (!isRunning) {
    Serial.println("\nSystem halted. Restart ESP32 to resume.");
    while (true);
  }

  if (WiFi.status() != WL_CONNECTED) {
    reconnectWiFi();
  }
  
  if (Serial.available() > 0) {
    String input = Serial.readString();
    input.trim();

    if (input == "register") {
      isRegistrationMode = true;
      getUserType();
      Serial.println("\nSwitching to Registration Mode. Scan a card to register.");
    } else if (input == "scan") {
      isRegistrationMode = false;
      getUserType();
      Serial.println("\nSwitching to Scan Mode. Scan a card to log attendance.");
    } else if (input == "exit") {
      Serial.println("\nExiting program. System halted.");
      isRunning = false;
    }
  }

  if (isRunning && mfrc522.PICC_IsNewCardPresent() && mfrc522.PICC_ReadCardSerial()) {
    String uid = getUID();
    Serial.println("NFC UID: " + uid);

    if (isRegistrationMode) {
      Serial.println("Enter the id:");
      while(!Serial.available());
      String id=Serial.readStringUntil('\n');
      id.trim();

      Serial.println("Enter User Name:");
      while (!Serial.available());
      String name = Serial.readStringUntil('\n');
      name.trim();

      Serial.println("Enter Gender (Male/Female/Other):");
      while (!Serial.available());
      String gender = Serial.readStringUntil('\n');
      gender.trim();

      if (name.length() > 0 && gender.length() > 0) {
        registerCard(id, uid, name, gender, role);
      } else {
        Serial.println("Invalid input. Please try again.");
      }
    } else {
      logAttendance(uid);
    }

    mfrc522.PICC_HaltA();  
    delay(1000);
  }
}

void getUserType() {
  Serial.println("Select Role: Type 'teacher' or 'student'");

  unsigned long startTime = millis();
  while (Serial.available() == 0) {
    if (millis() - startTime > 10000) {
      Serial.println("No input received. Defaulting to 'student'.");
      role = "student";
      return;
    }
  }

  role = Serial.readStringUntil('\n');  
  role.trim();
  role.toLowerCase();

  if (role != "teacher" && role != "student") {
    Serial.println("Invalid choice. Defaulting to 'student'.");
    role = "student";
  }

  Serial.print("Selected Role: ");
  Serial.println(role);
}


void registerCard(String id, String uid, String name, String gender, String role) {
String payload = "{\"id\":\"" + id + "\", \"name\":\"" + name + "\",\"uid\":\"" + uid + "\",\"gender\":\"" + gender + "\",\"role\":\"" + role + "\", \"attendance\":\"absent\"}";


  HTTPClient http;
  http.begin(registerEndpoint);
  http.addHeader("Content-Type", "application/json");

  int httpResponseCode = http.POST(payload);
  String response = http.getString();

  Serial.println("Server Response: " + response);

  if (httpResponseCode == 201) {
    Serial.println("Card Registered Successfully!");
  } else if (httpResponseCode == 409) {
    Serial.println("Registration Failed: Card already registered.");
  } else {
    Serial.println("Registration Error: " + String(httpResponseCode));
  }
  http.end();
}

void logAttendance(String uid) {
  String payload = "{\"uid\":\"" + uid + "\",\"role\":\"" + role + "\", \"attendance\":\"present\"}";

  HTTPClient http;
  http.begin(scanEndpoint);
  http.addHeader("Content-Type", "application/json");

  int httpResponseCode = http.POST(payload);
  String response = http.getString();

  Serial.println("Server Response: " + response);

  if (httpResponseCode == 200) {
    Serial.println("Attendance Logged Successfully!");
  } else if (httpResponseCode == 404) {
    Serial.println("User not found. Please register the card first.");
  } else {
    Serial.println("Attendance Error: " + String(httpResponseCode));
  }
  http.end();
}

String getUID() {
  String uid = "";
  for (byte i = 0; i < mfrc522.uid.size; i++) {
    uid += String(mfrc522.uid.uidByte[i] < 0x10 ? "0" : "") + String(mfrc522.uid.uidByte[i], HEX);
  }
  uid.toUpperCase();
  return uid;
}
