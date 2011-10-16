// Priyesh Patel

#include <LiquidCrystal.h>

LiquidCrystal lcd(12,11,5,4,3,2);

void setup()
{
  lcd.begin(16,2);
  lcd.print("Apex Alpha");
  
  Serial.begin(19200);
  
  lcd.setCursor(0,1);
  lcd.print("Altitude:      m");
}

void loop()
{
  if(Serial.available() >= 10)
  {
    for(int i = 0; i < 5; i++) { Serial.read(); }
    for(int i = 0; i < 5; i++)
    {
      lcd.setCursor(10+i,1);
      lcd.write(Serial.read());
    }
    Serial.flush();   
  }
}
