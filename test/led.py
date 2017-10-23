import RPi.GPIO as GPIO
import time

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(7, GPIO.OUT)

def blink(numTimes, speed):
        for i in range(0, numTimes):
                GPIO.output(7, True)
                time.sleep(speed)
                GPIO.output(7, False)
                time.sleep(speed)


#GPIO.cleanup

