#include <Servo.h>

Servo myservo;  
int pos = 0;    

void setup() {
  myservo.attach(9);  
  Serial.begin(9600); 
  Serial.println("Servo Initialized");
}

void loop() {
  if (Serial.available() > 0) {
    char command = Serial.read();
    if (command == '1') {
      // Rotate the servo to position 90 degrees for Person1
      Serial.println("Moving servo to 90 degree");
      myservo.write(90);
      delay(1000);  // Wait for 1 second
    } else if (command == '2') {
      // Rotate the servo to position 180 degrees for Person2
      Serial.println("Moving servo to 180 degree");
      myservo.write(180);
      delay(1000);  // Wait for 1 second
    } else {
      // Rotate the servo to position 0 degrees for all other cases
      Serial.println("Moving servo to 0 degree");
      myservo.write(0);
      delay(1000);  // Wait for 1 second
    }
  }
}
