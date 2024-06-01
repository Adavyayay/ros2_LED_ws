void setup() {
  Serial.begin(9600);
  pinMode(10, OUTPUT);
}

void loop() {
  if (Serial.available() > 0) {
    String command = Serial.readStringUntil('\n');
    command.trim();
    if (command == "ON") {
      digitalWrite(10, HIGH);
    } else if (command == "OFF") {
      digitalWrite(10, LOW);
    }
  }
}
