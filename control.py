from gpioSetup import *
import json
import random

class Control:
    def toggleHeater(self):
        if (gpio.input(PIN_HEAT_A) == 1):
            gpio.output(PIN_HEAT_A, False)
            gpio.output(PIN_HEAT_B, True)
        else:
            gpio.output(PIN_HEAT_A, True)
            gpio.output(PIN_HEAT_B, False)
            
    def isHeatOn(self) -> bool:
        print("isHeatOn=", gpio.input(PIN_HEAT_ON))
        return gpio.input(PIN_HEAT_ON) == 1

    def getTemp(self):
        return str(round(random.uniform(-20, 110), 3))
