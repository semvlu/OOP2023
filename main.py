import time
from time import sleep_ms

import machine
from machine import Pin, I2C
from Fan import Fan
from Drip import Drip
from Led import Led
from i2c_lcd import I2cLcd
import dht
DEFAULT_I2C_ADDR = 0x27

tempHyg = dht.DHT11(machine.Pin(17)) # thermometre & hygrometre
gas = Pin(23, Pin.IN, Pin.PULL_UP)
drip = Drip()
fan = Fan()
led = Led(200)
i2c = I2C(scl=Pin(22), sda=Pin(21), freq=400000) 
lcd = I2cLcd(i2c, DEFAULT_I2C_ADDR, 2, 16)

pin = Pin(26, Pin.OUT) # did not use it

try:
    while True:
        volt = drip.volt()
        print("ADC Val: ", drip.val(),"DAC Val:", drip.dac(),"Voltage:", volt,"V")
        tempHyg.measure()
        print('Temperature:',tempHyg.temperature(),'℃','Humidity:',tempHyg.humidity(),'%')

        lcd.move_to(1, 0)
        lcd.putstr('T= {}'.format(tempHyg.temperature()))
        lcd.move_to(1, 1)
        lcd.putstr('H= {}'.format(tempHyg.humidity()))
        time.sleep_ms(10)

        led.norm()
        if(volt > 2):
            led.rain()

        gasVal = gas.value()
        print("Gas: ", gasVal)

        if(gasVal != 1): # gas leak
            led.gasLeak()
            fan.run()
except:
    fan.INA.duty(0)
    fan.INB.duty(0)
    fan.INA.deinit()
    fan.INB.deinit()