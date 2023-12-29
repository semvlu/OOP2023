import neopixel
import time
from time import sleep_ms 

class Led():
    def __init__(self, bri):
        self.np = neopixel.NeoPixel(pin, 4) 
        self.colors=[[bri,0,0], #R
        [0,bri,0],  #G
        [0,0,bri], #B
        [bri,bri,bri], #White
        [0,0,0]] # off

    def norm(self):
        for i in range(0,5):
            for j in range(0,4):
                self.np[j]=self.colors[i]
                self.np.write()
                time.sleep_ms(50)
            time.sleep_ms(50)
        time.sleep_ms(50)

    def rain(self):
        self.np[0]=self.colors[2]
        self.np.write()
        self.np[1]=self.colors[2]
        self.np.write()
        self.np[2]=self.colors[2]
        self.np.write()
        self.np[3]=self.colors[2]
        self.np.write()

    def gasLeak(self):
        self.np[0]=self.colors[0]
        self.np.write()
        self.np[1]=self.colors[0]
        self.np.write()
        self.np[2]=self.colors[0]
        self.np.write()
        self.np[3]=self.colors[0]
        self.np.write()

