from gpioSetup import *
import json
import random
import glob
import time

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


    def read_temp_raw() -> float:
        tempDevice = glob.glob('/sys/bus/w1/devices/28*')[0]
        tf = open(tempDevice + '/w1_slave', 'r')
        lines = tf.readlines()
        tf.close()
        return lines


    def getTemp(self) -> float:
        print('getTemp()')
        lines = Control.read_temp_raw()
        if (lines[0].strip()[-3:] != 'YES'):
            return 999

        equals_pos = lines[1].find('t=')
        if equals_pos != -1:
            temp_string = lines[1][equals_pos+2:]
            temp_c = float(temp_string) / 1000.0
            temp_f = temp_c * 9.0 / 5.0 + 32.0
            return temp_f
        return 999

