Python 3.4.2 (default, Oct 19 2014, 13:31:11) 
[GCC 4.9.1] on linux
Type "copyright", "credits" or "license()" for more information.
>>> print "hello"
SyntaxError: Missing parentheses in call to 'print'
>>> print ("hello")
hello
>>> import RPi.GPIO as GPIO
>>> GPIO.VER
Traceback (most recent call last):
  File "<pyshell#3>", line 1, in <module>
    GPIO.VER
AttributeError: 'module' object has no attribute 'VER'
>>> 
>>> GPIO.VERSION
'0.6.3'
>>> GPIO.setm
Traceback (most recent call last):
  File "<pyshell#6>", line 1, in <module>
    GPIO.setm
AttributeError: 'module' object has no attribute 'setm'
>>> GPIO.setmode(GPIO.BOARD)
>>> GPIO.setup(10, GPIO.OUT)

Warning (from warnings module):
  File "__main__", line 1
RuntimeWarning: This channel is already in use, continuing anyway.  Use GPIO.setwarnings(False) to disable warnings.
>>> GPIO.output(10,true)
Traceback (most recent call last):
  File "<pyshell#9>", line 1, in <module>
    GPIO.output(10,true)
NameError: name 'true' is not defined
>>> GPIO.output(10,True)
>>> GPIO.output(10,False)
>>> GPIO.output(10,True)
>>> GPIO.setup(7, GPIO.OUT0
	   
KeyboardInterrupt
>>> GPIO.setup(7, GPIO.OUT)
>>> GPIO.output(7, True)
>>> GPIO.output(7, False)
>>> GPIO.output(7, True)
>>> GPIO.output(7, False)
>>> for i in range(0, 10):
	print "Blink " + i
	
SyntaxError: Missing parentheses in call to 'print'
>>> for i in range(0, 10):
	print("Blink " + i)
	GPIO.output(7, True)
	time.sleep(1)
	GPIO.output(7, False)
	time.sleep(1)
import time
SyntaxError: invalid syntax
>>> def blink(numTimes, speed):
	for i in range(0, numTimes):
		print("Blink " + str(i+1))
		GPIO.output(7, True)
		time.sleep(speed)
		GPIO.output(7, False)
		time.sleep(speed)
	print ("Done")
	GPIO.cleanup

	
>>> blink(3, 1)
Blink 1
Traceback (most recent call last):
  File "<pyshell#32>", line 1, in <module>
    blink(3, 1)
  File "<pyshell#31>", line 5, in blink
    time.sleep(speed)
NameError: name 'time' is not defined
>>> import time
>>> blink(3, 1)
Blink 1
Blink 2
Blink 3
Done
>>> blink(3,.25)
Blink 1
Blink 2
Blink 3
Done
>>> 
