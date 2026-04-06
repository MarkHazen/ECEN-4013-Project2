String InBytes;

void setup() {
  // Serial setup
  Serial.begin(9600);

  // LED output setup
  pinMode(13, OUTPUT);
}

// Control Loop
void loop() {
  if (Serial.available() > 0) {
    // Recieves data from serial
    InBytes = Serial.readStringUntil('\n');

    // Checks command and changes LED Value
    if (InBytes == "on") {
      digitalWrite(13, HIGH);
      Serial.write("LED on");
    } else if (InBytes == "off") {
      digitalWrite(13, LOW);
      Serial.write("LED off");
    } else {
      Serial.write("Invalid Input");
    }
  }
}