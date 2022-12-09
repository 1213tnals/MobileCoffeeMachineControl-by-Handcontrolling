#define DIR1 2
#define PWM1 3
#define DIR2 4
#define PWM2 5  //Driving motors

char mode_sub = 'Z';
int left_speed_int = 0;
int right_speed_int = 0;

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  pinMode(LED_BUILTIN, OUTPUT);

  pinMode(DIR1, OUTPUT);
  pinMode(PWM1, OUTPUT);
  pinMode(DIR2, OUTPUT);
  pinMode(PWM2, OUTPUT);
}

void loop() {
  // put your main code here, to run repeatedly:
  if (Serial.available()) {
    mode_sub = Serial.read();
    
    if (mode_sub == 'S')           //stop and water pump opertion ready
    {
      left_speed_int = 0;
      right_speed_int = 0;
      digitalWrite(DIR1, HIGH);
      analogWrite(PWM1, left_speed_int);
      digitalWrite(DIR2, HIGH);
      analogWrite(PWM2, right_speed_int);
      Serial.print("motor_speed");
      Serial.print("left_speed_int: ");
      Serial.print(left_speed_int);
      Serial.print("  /  ");
      Serial.print("right_speed_int: ");
      Serial.println(right_speed_int);
      delay(1000);

      while(mode_sub != 'R')
      {
        mode_sub = Serial.read();

        if (mode_sub == 'A')        
        {       
          Serial.println("shot1");          
          delay(2000);
        }
        else if (mode_sub == 'B')        
        {       
          Serial.println("shot2");          
          delay(2000);
        }
        else if (mode_sub == 'C')        
        {       
          Serial.println("shot3");          
          delay(2000);
        }
      }
    }

    if (mode_sub == 'D')            //left
    {       
      left_speed_int = 20;
      right_speed_int = 60;
    }
    else if (mode_sub == 'E')
    {
      left_speed_int = 30;
      right_speed_int = 70;
    }
    else if (mode_sub == 'F')
    {
      left_speed_int = 40;
      right_speed_int = 80;
    }
    
    else if (mode_sub == 'G')        //right
    {    
      left_speed_int = 60;
      right_speed_int = 20;
    }
    else if (mode_sub == 'H')
    {
      left_speed_int = 70;
      right_speed_int = 30;
    }
    else if (mode_sub == 'I')
    {
      left_speed_int = 80;
      right_speed_int = 40;
    }
    else if (mode_sub == 'J')        //forward
    {
      left_speed_int = 60;
      right_speed_int = 60;
    }
    else if (mode_sub == 'K')
    {
      left_speed_int = 70;
      right_speed_int = 70;
    }
    else if (mode_sub == 'L')
    {
      left_speed_int = 80;
      right_speed_int = 80;
    }
    
    digitalWrite(DIR1, HIGH);
    analogWrite(PWM1, left_speed_int);
    digitalWrite(DIR2, HIGH);
    analogWrite(PWM2, right_speed_int);
    Serial.print("motor_speed");
    Serial.print("left_speed_int: ");
    Serial.print(left_speed_int);
    Serial.print("  /  ");
    Serial.print("right_speed_int: ");
    Serial.println(right_speed_int);

  }
}
