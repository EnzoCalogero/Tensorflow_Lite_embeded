from time import sleep
from adafruit_servokit import ServoKit
kit = ServoKit(channels=16)
kit.servo[0].angle = 170
kit.servo[1].angle = 170
sleep(1)
kit.servo[0].angle = 10
kit.servo[1].angle = 10
