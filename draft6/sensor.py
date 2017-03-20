import RPi.GPIO as GPIO
import time

global infrared, ultrasonic, servomotor, motor_L1, motor_L2, motor_R1, motor_R2, servo_turning_time, outputpin, carspeed, sensor_infrared, sensor_on, gpiodidstartup
infrared = 11
ultrasonic = 8
servomotor = 12
motor_L1 = 19
motor_L2 = 21
motor_R1 = 24
motor_R2 = 26
servo_turning_time = 0.5
carspeed = 100
sensor_infrared = False
sensor_on = True

def gpio_startup():
    global a1,a2,b1,b2,gpiodidstartup, p
    GPIO.setmode(GPIO.BOARD)
    inputpin = [infrared,ultrasonic]
    outputpin = [servomotor,motor_L1,motor_L2,motor_R1,motor_R2]
    GPIO.setup(inputpin,GPIO.IN)
    GPIO.setup(outputpin,GPIO.OUT,initial = GPIO.LOW)
    a1 = GPIO.PWM(motor_L1, 50)
    a2 = GPIO.PWM(motor_L2, 50)
    b1 = GPIO.PWM(motor_R1, 50)
    b2 = GPIO.PWM(motor_R2, 50)
    gpiodidstartup = True
    p = GPIO.PWM(servomotor,50)

def gpio_end():
    GPIO.cleanup()
    print("all GPIO pin is clean up")


def sensor_if():
    global sensor_infrared
    if GPIO.IN(infrared) == 1:
        sensor_infrared = True
    elif GPIO.IN(infrared) == 0:
        sensor_infrared = False
    else:
        print("infrared sensor error")
    pass


def sensor_ultrasonic():
    global detect_distance
    GPIO.setup(ultrasonic, GPIO.OUT)
    GPIO.output(ultrasonic, GPIO.HIGH)
    time.sleep(0.00001)
    GPIO.output(ultrasonic, GPIO.LOW)
    start = time.time()
    count = time.time()
    GPIO.setup(ultrasonic, GPIO.IN)
    while GPIO.input(ultrasonic) == 0 and time.time() - count < 0.1:
        start = time.time()

    count = time.time()
    stop = count
    while GPIO.input(ultrasonic) == 1 and time.time() - count < 0.1:
        stop = time.time()
    # Calculate pulse length
    elapsed = stop - start
    # Distance pulse travelled in that time is time
    # multiplied by the speed of sound (cm/s)
    distance = elapsed * 34000
    # That was the distance there and back so halve the value
    distance = distance / 2
    detect_distance = distance
    return detect_distance


def motor_turn_left():
    p.start(5)
    time.sleep(servo_turning_time)
    p.stop()
    pass


def motor_turn_right():
    p.start(10)
    time.sleep(servo_turning_time)
    p.stop()
    pass


def motor_netural():
    p.start(7.5)  #dutycycle of netural
    time.sleep(servo_turning_time)
    p.stop()
    pass


def motor_stop():
    p.stop()
    a1.stop()
    a2.stop()
    b1.stop()
    b2.stop()
    pass


def motor_forward(carspeed = carspeed):
    a1.start(0)
    b1.start(0)
    a1.start(carspeed)
    b1.start(carspeed)
    pass


def motor_backward(carspeed = carspeed):
    a2.start(0)
    b2.start(0)
    a2.start(carspeed)
    b2.start(carspeed)
    pass


def change_speed(direction,speed):  #1 for forward 2 for backward, anyother number will result in error
    carspeed = speed
    if direction == 1:
        motor_forward(carspeed)
    elif direction == 2:
        motor_backward(carspeed)
    else:
        print('Direction error')


def collision_prevention_system():
    sensor_infrared == False
    sensor_on = False
    while sensor_on:
        sensor_ultrasonic()
        sensor_if()

        if  sensor_infrared == True:
            a1.stop()
            b1.stop()
            a2.stop()
            b2.stop()

def testing_deletlater():
    global detect_distance,sensor_infrared
    detect_distance = 0
    sensor_infrared = 0
    while True:
            print(detect_distance)
            print(sensor_infrared)
