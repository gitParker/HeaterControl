import random

class Control:
    def __init__(self):
        self.heatOn = False;

    def toggleHeater(self):
       self.heatOn = not self.heatOn
            
    def isHeatOn(self) -> bool:
        print("isHeatOn=", self.heatOn)
        return self.heatOn

    def getTemp(self):
        return str(round(random.uniform(50, 105), 3))
