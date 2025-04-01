#include <Wire.h>

// Motor control pins
const int enA = 6;  // Enable motor A
const int in1 = 4;  // Motor A input 1
const int in2 = 5;  // Motor A input 2
const int in3 = 7;  // Motor B input 1
const int in4 = 8;  // Motor B input 2
const int enB = 9;  // Enable motor B

// Buzzer and button pins
const int buzzer = A0;
const int startButton = 12;

// I2C address
#define SLAVE_ADDRESS 0x08

// Variables
bool systemActive = true;    // System always active by default
int currentSpeed = 200;      // Current motor speed (0-255)
unsigned long lastActivityTime = 0;
const unsigned long WATCHDOG_TIMEOUT = 15000;  // 15 second timeout

void setup() {
  // Initialize motor control pins
  pinMode(enA, OUTPUT);
  pinMode(in1, OUTPUT);
  pinMode(in2, OUTPUT);
  pinMode(in3, OUTPUT);
  pinMode(in4, OUTPUT);
  pinMode(enB, OUTPUT);
  
  // Initialize buzzer and button
  pinMode(buzzer, OUTPUT);
  pinMode(startButton, INPUT_PULLUP);
  
  // Set initial motor speed
  analogWrite(enA, currentSpeed);
  analogWrite(enB, currentSpeed);
  
  // Start hardware serial (for debugging)
  Serial.begin(9600);
  
  // Initialize I2C
  Wire.begin(SLAVE_ADDRESS);
  Wire.onReceive(receiveEvent);
  
  // Initial state
  stopMotors();
  
  // Short beep to indicate boot
  beep(100);  
  delay(100);
  
  Serial.println("BOOT:READY");
  Serial.println("System is ACTIVE by default");

  // Double beep to indicate ready
  beep(100);
  delay(100);
  beep(100);
  
  lastActivityTime = millis();
}

void loop() {
  // Button now just stops motors for safety (instead of toggle)
  if (digitalRead(startButton) == LOW) {
    stopMotors();
    beep(150);  // Feedback beep
    delay(200);  // Longer debounce
    Serial.println("Emergency stop via button");
  }
  
  // Check for watchdog timeout
  if (millis() - lastActivityTime > WATCHDOG_TIMEOUT) {
    Serial.println("WATCHDOG: Timeout - stopping motors");
    stopMotors();
    beep(800);  // Long warning beep
    lastActivityTime = millis(); // Reset the timer
  }
}

void receiveEvent(int howMany) {
  if (Wire.available()) {
    char command = Wire.read();
    processCommand(command);
  }
}

void processCommand(char command) {
  lastActivityTime = millis();  // Reset watchdog timer
  String response;
  
  // Echo command for verification
  Serial.print("CMD: ");
  Serial.println(command);
  
  // Process based on command character
  switch (command) {
    case 'F': // Forward
      forward();
      response = "ACK:FWD";
      break;
      
    case 'B': // Backward
      backward();
      response = "ACK:BWD";
      break;
      
    case 'L': // Left
      turnLeft();
      response = "ACK:LEFT";
      break;
      
    case 'R': // Right
      turnRight();
      response = "ACK:RIGHT";
      break;
      
    case 'S': // Stop
      stopMotors();
      response = "ACK:STOP";
      break;
      
    case '0'...'9': // Speed
      int speedLevel = command - '0';
      setSpeed(map(speedLevel, 0, 9, 50, 255));  // Map 0-9 to 50-255
      response = "ACK:SPD:" + String(speedLevel);
      break;
      
    case 'X': // No longer toggles - just a status indicator
      response = "ACK:SYS:ON";
      break;
      
    case '?': // Status
      response = "STAT:ON:SPD:" + String(map(currentSpeed, 50, 255, 0, 9));
      break;
      
    default:
      response = "ERR:INVALID";
      break;
  }
  
  // Log response to serial for debugging
  Serial.println(response);
}

// Motor control functions
void forward() {
  digitalWrite(in1, LOW);
  digitalWrite(in2, HIGH);
  digitalWrite(in3, HIGH);
  digitalWrite(in4, LOW);
}

void backward() {
  digitalWrite(in1, HIGH);
  digitalWrite(in2, LOW);
  digitalWrite(in3, LOW);
  digitalWrite(in4, HIGH);
}

void turnLeft() {
  digitalWrite(in1, HIGH);
  digitalWrite(in2, LOW);
  digitalWrite(in3, HIGH);
  digitalWrite(in4, LOW);
}

void turnRight() {
  digitalWrite(in1, LOW);
  digitalWrite(in2, HIGH);
  digitalWrite(in3, LOW);
  digitalWrite(in4, HIGH);
}

void stopMotors() {
  digitalWrite(in1, LOW);
  digitalWrite(in2, LOW);
  digitalWrite(in3, LOW);
  digitalWrite(in4, LOW);
}

void setSpeed(int speed) {
  currentSpeed = constrain(speed, 0, 255);
  analogWrite(enA, currentSpeed);
  analogWrite(enB, currentSpeed);
}

void beep(int duration) {
  tone(buzzer, 1000, duration);
} 