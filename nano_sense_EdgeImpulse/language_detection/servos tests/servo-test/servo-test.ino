/*************************************************** 
  This is an example for our Adafruit 16-channel PWM & Servo driver
  Servo test - this will drive 8 servos, one after the other on the
  first 8 pins of the PCA9685

  Pick one up today in the adafruit shop!
  ------> http://www.adafruit.com/products/815
  
  These drivers use I2C to communicate, 2 pins are required to  
  interface.

  Adafruit invests time and resources providing this open source code, 
  please support Adafruit and open-source hardware by purchasing 
  products from Adafruit!

  Written by Limor Fried/Ladyada for Adafruit Industries.  
  BSD license, all text above must be included in any redistribution
 ****************************************************/

#include <Wire.h>
#include <Adafruit_PWMServoDriver.h>

// called this way, it uses the default address 0x40
Adafruit_PWMServoDriver pwm = Adafruit_PWMServoDriver();
// you can also call it with a different address you want
//Adafruit_PWMServoDriver pwm = Adafruit_PWMServoDriver(0x41);
// you can also call it with a different address and I2C interface
//Adafruit_PWMServoDriver pwm = Adafruit_PWMServoDriver(0x40, Wire);

// Depending on your servo make, the pulse width min and max may vary, you 
// want these to be as small/large as possible without hitting the hard stop
// for max range. You'll have to tweak them as necessary to match the servos you
// have!
#define SERVOMIN  200 // This is the 'minimum' pulse length count (out of 4096)
#define SERVOMAX  350//600 // This is the 'maximum' pulse length count (out of 4096)
#define USMIN  600 // This is the rounded 'minimum' microsecond length based on the minimum pulse of 150
#define USMAX  2400 // This is the rounded 'maximum' microsecond length based on the maximum pulse of 600
#define SERVO_FREQ 50 // Analog servos run at ~50 Hz updates

// our servo # counter
// uint8_t servonum = 0;
int iter;
int period = 1000;
unsigned long time_now = 0;
unsigned long time_was = 0;

unsigned long delta;
void servos_selector(int iter){
  
  time_now = millis();
  Serial.println(iter);
  
  Serial.println(time_now);
  delta=time_now - time_was;
  Serial.println(delta);
  Serial.println("#################");
  if (delta > 5000){
    time_was=time_now;
  switch (iter) {
       case 0:
            pwm.setPWM(0, 0, 350);
            Serial.println("111");
            delay(500);
            pwm.setPWM(0, 0, 200);
            pwm.setPWM(1, 0, 200);
            pwm.setPWM(2, 0, 200);
            break;
      case 1:
            pwm.setPWM(1, 0, 350);
            Serial.println("2222");
            delay(500);
            pwm.setPWM(0, 0, 200);
            pwm.setPWM(1, 0, 200);
            pwm.setPWM(2, 0, 200);
            break;
      case 2:
            pwm.setPWM(2, 0, 350);
            Serial.println("333");
            delay(500);
            pwm.setPWM(0, 0, 200);
            pwm.setPWM(1, 0, 200);
            pwm.setPWM(2, 0, 200);
            break;
  }
  }
}

void setup() {
  Serial.begin(9600);
  Serial.println("8 channel Servo test!");

  pwm.begin();
  pwm.setOscillatorFrequency(27000000);
  pwm.setPWMFreq(SERVO_FREQ);  // Analog servos run at ~50 Hz updates

  delay(100);
}


void loop() {
for(iter=0; iter < 4; iter++){  
servos_selector(iter);
delay(5);
  }
}
