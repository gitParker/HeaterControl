import RPi.GPIO as gpio

PIN_HEAT_A = 7
PIN_HEAT_B = 11
PIN_HEAT_ON = 13
PIN_TEMP_IN = 15

gpio.setwarnings(False)
gpio.setmode(gpio.BOARD)
gpio.setup(PIN_HEAT_A, gpio.OUT)
gpio.setup(PIN_HEAT_B, gpio.OUT)
#gpio.setup(PIN_HEAT_ON, gpio.IN)
gpio.setup(PIN_TEMP_IN, gpio.IN)

gpio.setup(PIN_HEAT_ON, gpio.IN, pull_up_down=gpio.PUD_UP)
#gpio.add_event_detect(PIN_HEAT_ON, gpio.BOTH, callback=toggle_callback, bouncetime=300)
