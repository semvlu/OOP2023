import time
import machine
from time import sleep_ms, ticks_ms 
from machine import Pin, PWM, I2C, ADC, DAC
from i2c_lcd import I2cLcd
import dht
import neopixel
DEFAULT_I2C_ADDR = 0x27

#-------move to Drip---------
#打開ADC並配置0-3.3V的範圍
adc = ADC(Pin(34))
adc.atten(ADC.ATTN_11DB)
adc.width(ADC.WIDTH_12BIT)
#------------------------


DHT = dht.DHT11(machine.Pin(17))
gas = Pin(23, Pin.IN, Pin.PULL_UP)

i2c = I2C(scl=Pin(22), sda=Pin(21), freq=400000) 
lcd = I2cLcd(i2c, DEFAULT_I2C_ADDR, 2, 16)

#-----move to Fan--------------
# 2 pins of the motor
INA =PWM(Pin(19,Pin.OUT),10000,0) # IN+
INB =PWM(Pin(18,Pin.OUT),10000,2) # IN-
#------------------------

pin = Pin(26, Pin.OUT) #did not use 

#---------move to Led-------------
np = neopixel.NeoPixel(pin, 4) 

#亮度:0 - 255
brightness=10                                
colors=[[brightness,0,0],                    #红
        [0,brightness,0],                    #绿
        [0,0,brightness],                    #蓝
        [brightness,brightness,brightness],  #白
        [0,0,0]]                             #关闭
#---------------------------------

try:
    while True:
        #-----move to Drip--------
        adcVal = adc.read()
        dacVal = adcVal//16
        voltage = adcVal / 4095.0 * 3.3
        print("ADC Val:", adcVal,"DACVal:", dacVal,"Voltage:", voltage,"V")
        #------------------------

        DHT.measure()
        #調用DHT的內置函數獲取溫度和濕度數據
        print('temperature:',DHT.temperature(),'℃','humidity:',DHT.humidity(),'%')

        lcd.move_to(1, 0)
        lcd.putstr('T= {}'.format(DHT.temperature()))
        lcd.move_to(1, 1)
        lcd.putstr('H= {}'.format(DHT.humidity()))
        time.sleep_ms(10)

        #------move to Led.norm()------------
        for i in range(0,5):
            for j in range(0,4):
                np[j]=colors[i]
                np.write()
                time.sleep_ms(50)
            time.sleep_ms(50)
        time.sleep_ms(50)
        #-----------------------

        #------move to Led.rain()------------
        if(voltage > 2):
            np[0]=colors[2]
            np.write()
            np[1]=colors[2]
            np.write()
            np[2]=colors[2]
            np.write()
            np[3]=colors[2]
            np.write()
        #----------------------------



        gasVal = gas.value()#讀取MQ-2的值
        print("Gas: ", gasVal)

        if(gasVal != 1): # dangerous
            #-------move to Led.gasLeak()------------
            np[0]=colors[0]
            np.write()
            np[1]=colors[0]
            np.write()
            np[2]=colors[0]
            np.write()
            np[3]=colors[0]
            np.write()
            #---------------------------
            
            #-------move to Fan.run()---------
            INA.duty(0) # 占空比范围为0-1023
            INB.duty(700)#逆時針轉
            time.sleep(10) # run 10 secs
            INA.duty(0)
            INB.duty(0)
            #-----------------------------------
            
except:
    INA.duty(0)
    INB.duty(0)
    INA.deinit()
    INB.deinit()