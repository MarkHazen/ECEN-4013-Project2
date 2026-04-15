void setup() {
  Serial1.begin(9600); // Default baud for HC-05 is 9600
}
void loop() {
  Serial1.println("Data from Adalogger");
  delay(1000);
}
