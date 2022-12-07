#define DIR1 2
#define PWM1 3
#define DIR2 4
#define PWM2 5  //Driving motors

char speed_sub = 'Z';
int speed_int = 0;

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
    speed_sub = Serial.read();

    if (speed_sub == 'A') {
      speed_int = 60;
    }
    else if (speed_sub == 'B') {
      speed_int = 80;
    }
    else if (speed_sub == 'C') {
      speed_int = 100;
    }
    digitalWrite(DIR1, HIGH);
    analogWrite(PWM1, speed_int);
    digitalWrite(DIR2, HIGH);
    analogWrite(PWM2, speed_int);
    Serial.print("motor_speed");
    Serial.println(speed_int);
  }
}
