#define DIR1 2
#define PWM1 3
#define DIR2 4
#define PWM2 5  //Driving motors

int speed;

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
  if(Serial.available()){
    speed = Serial.read();

    digitalWrite(DIR1, HIGH);
    analogWrite(PWM1, speed);
    digitalWrite(DIR2, HIGH);
    analogWrite(PWM2, speed);
    Serial.print("motor_speed");
    Serial.println(speed);
  }
}
