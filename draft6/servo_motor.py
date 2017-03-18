
import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BOARD)

GPIO.setup(11,GPIO.OUT,initial =GPIO.LOW)
GPIO.setup(15,GPIO.IN)

def mode1():
    GPIO.output(11, GPIO.HIGH)
    time.sleep(0.01)
    GPIO.output(11, GPIO.LOW)
    print("GPIOstart")

def mode2():
    p = GPIO.PWM(11,50)
    p.start(10) #control the speed of turning 1 is fastest, 100 is the slowest
    time.sleep(30)
    p.stop()
    print("end")

def mode3():
    p = GPIO.PWM(11,50)
    p.start(0)
    p.ChangeDutyCycle(7) #This is the position the servo will switch 2
    time.sleep(1)
    p.stop(10)
    print("end")

mode3()

while False:
    if GPIO.input(15):
     print("high")
    else:
     print("low")


GPIO.cleanup()
