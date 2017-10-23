from gpioSetup import *
import json

class Control:
##    def __init__(self):
##        self.heatOn = False;

##    def toggleHeater(self):
##       self.heatOn = not self.heatOn

    def toggleHeater(self):
        if (gpio.input(PIN_HEAT_A) == 1):
            gpio.output(PIN_HEAT_A, False)
            gpio.output(PIN_HEAT_B, True)
        else:
            gpio.output(PIN_HEAT_A, True)
            gpio.output(PIN_HEAT_B, False)
            
    def isHeatOn(self) -> bool:
##        print("isHeatOn=", self.heatOn)
##        return self.heatOn
        print("isHeatOn=", gpio.input(PIN_HEAT_ON))
        return gpio.input(PIN_HEAT_ON) == 1
