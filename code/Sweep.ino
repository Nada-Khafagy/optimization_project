
#include <Servo.h>

Servo motor1;
Servo motor2;
Servo motor3;
Servo motor4;
int pos = 0;
void setup() {

  motor1.attach(11);   // Attach motor1 to pin 9
  motor2.attach(10);  // Attach motor2 to pin 10
  
  motor3.attach(6);  // Attach motor4 to pin 12
  motor4.attach(10);  // Attach motor3 to pin 9
  Serial.begin(9600);
}

void loop() {
  for (pos = 0; pos <= 40; pos += 1) { // goes from 0 degrees to 180 degrees
    // in steps of 1 degree
    motor1.write(pos);              // tell servo to go to position in variable 'pos'
    delay(15);                       // waits 15 ms for the servo to reach the position
  }

  for (pos = 40; pos >= 0; pos -= 1) { // goes from 180 degrees to 0 degrees
    motor1.write(pos);              // tell servo to go to position in variable 'pos'
    delay(15);                       // waits 15 ms for the servo to reach the position
  }


  for (pos = 40; pos >= 0; pos -= 1) { // goes from 180 degrees to 0 degrees
    motor2.write(pos);              // tell servo to go to position in variable 'pos'
    delay(15);                       // waits 15 ms for the servo to reach the position
  }


   for (pos = 0; pos <= 50; pos += 1) { // goes from 0 degrees to 180 degrees
    // in steps of 1 degree
    motor2.write(pos);              // tell servo to go to position in variable 'pos'
    delay(15);                       // waits 15 ms for the servo to reach the position
  }



 for (pos = 0; pos <= 30; pos += 1) { // goes from 0 degrees to 180 degrees
    // in steps of 1 degree
    motor3.write(pos);              // tell servo to go to position in variable 'pos'
    delay(15);       
 }
  for (pos = 30; pos >= 0; pos -= 1) { // goes from 180 degrees to 0 degrees
    motor3.write(pos);              // tell servo to go to position in variable 'pos'
    delay(15);       
}

for (pos = 30; pos <=0; pos -= 1) { // goes from 0 degrees to 180 degrees
    // in steps of 1 degree
    motor4.write(pos);              // tell servo to go to position in variable 'pos'
    Serial.write(pos); //اتحرق؟
    delay(15);
          
 }
 
  delay(100);
}