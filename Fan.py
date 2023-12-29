import time
from machine import Pin, PWM

class Fan:
    def __init__(self):
        # 2 pins of the motor
        self.INA =PWM(Pin(19,Pin.OUT),10000,0) # IN+
        self.INB =PWM(Pin(18,Pin.OUT),10000,2) # IN-
    def run(self):
        self.INA.duty(0) # 0-1023
        self.INB.duty(700)
        time.sleep(10) # run 10 secs
        self.INA.duty(0)
        self.INB.duty(0)