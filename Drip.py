from machine import ADC,Pin

class Drip:
    def __init__(self):
        # assign ADC, 0 - 3.3V
        self.adc = ADC(Pin(34))
        adc.atten(ADC.ATTN_11DB)
        adc.width(ADC.WIDTH_12BIT)

    def val(self):
        return self.adc.read()
    def dac(self):
        return self.val() // 16
    def volt(self):
        return self.val() / 4095.0 * 3.3