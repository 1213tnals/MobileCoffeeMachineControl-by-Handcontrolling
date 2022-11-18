char cmd;

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  pinMode(LED_BUILTIN, OUTPUT);
}

void loop() {
  // put your main code here, to run repeatedly:
  if(Serial.available()){
    cmd = Serial.read();

    if(cmd=='S'){
      Serial.println("Stop Motor");
      digitalWrite(LED_BUILTIN, HIGH);
      delay(5000);
    }

    if(cmd=='O'){
      Serial.println("User Finded");
      digitalWrite(LED_BUILTIN, HIGH);
      delay(5000);
    }
      
    if(cmd=='A'){
      Serial.println("You order Half shot");
      digitalWrite(LED_BUILTIN, HIGH);
      delay(2000);
    }
      
    if(cmd=='B'){
      Serial.println("You order One shot");
      digitalWrite(LED_BUILTIN, HIGH);
      delay(2000);
    }
      
    if(cmd=='C'){
      Serial.println("You order Two shot");
      digitalWrite(LED_BUILTIN, HIGH);
      delay(2000);
    }
  }
}
