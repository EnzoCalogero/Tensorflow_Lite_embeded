from time import sleep

import board
import busio
#import adafruit_pca9685
#i2c = busio.I2C(board.SCL, board.SDA)
#pca = adafruit_pca9685.PCA9685(i2c)

#led_channel = pca.channels[3]
#led_channel.duty_cycle = 0
#sleep(2)
#led_channel.duty_cycle = 0xffff


from adafruit_servokit import ServoKit
kit = ServoKit(channels=16)
#kit.servo[3].angle =170
#status=0
for status in {0,1,2,3,4}:
    if (status==0):
        kit.servo[0].angle = 0
        kit.servo[1].angle = 0
        kit.servo[2].angle = 0
    elif (status==1):
        kit.servo[0].angle = 90
        kit.servo[1].angle = 0
        kit.servo[2].angle = 0
    elif (status==2):
        kit.servo[0].angle = 0
        kit.servo[1].angle = 90
        kit.servo[2].angle = 0
    elif (status==3):
        kit.servo[0].angle = 0
        kit.servo[1].angle = 0
        kit.servo[2].angle = 90
    elif(status==4):
        kit.servo[0].angle = 90
        kit.servo[1].angle = 90
        kit.servo[2].angle = 90
    sleep(1)    
        