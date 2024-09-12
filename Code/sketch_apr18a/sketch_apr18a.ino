
#include <Wire.h>
#include <LiquidCrystal_I2C.h>

// Set the LCD address to 0x27 for a 16 chars and 2 line display
LiquidCrystal_I2C lcd(0x27, 16, 2);

int soilMoisturePin = A0;
int waterLevelPin = A1;
int pumpPin = 2;
int buzzerPin = 9;

void setup() {
  pinMode(pumpPin, OUTPUT);
  pinMode(buzzerPin, OUTPUT);
  Serial.begin(9600);
 
  lcd.init();                      // Initialize the lcd
  lcd.backlight();
  lcd.clear();
}

void loop() {
  digitalWrite(buzzerPin, HIGH);
  int soilMoisture = analogRead(soilMoisturePin);
  int waterLevel = analogRead(waterLevelPin);

  Serial.print("Soil Moisture: ");
  Serial.print(soilMoisture);
  Serial.print(", Water Level: ");
  Serial.println(waterLevel);

  // Display soil moisture and water level
  lcd.setCursor(0, 0);
  lcd.print("Moisture: ");
  lcd.print(soilMoisture);
  lcd.setCursor(0, 1);
  lcd.print("Water Lvl: ");
  lcd.print(waterLevel);

  if (waterLevel < 590) {
    digitalWrite(buzzerPin, HIGH);
    delay(100); // Buzzer on for 5 seconds
    digitalWrite(buzzerPin, LOW);
  }

  if (Serial.available() > 0) {
    String command = Serial.readStringUntil('\n');
    if (command == "TURN_ON_PUMP") {
      digitalWrite(pumpPin, HIGH);
      lcd.clear();
      lcd.setCursor(0, 1);
      lcd.print("Pump:ON ");
    }
    if (command == "TURN_OFF_PUMP") {
      digitalWrite(pumpPin, LOW);
      lcd.clear();
      lcd.setCursor(0, 1);
      lcd.print("Pump:OFF");
    }
  }

  delay(2000);
}
