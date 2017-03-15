import RPi.GPIO as GPIO
import time



def gpio_startup():
    #pin number for motor===============================================================================
    global infrared,ultrasonic,servomotor,motor_L1,motor_L2,motor_R1,motor_R2,p,servo_turning_time,outputpin,a1,a2,b1,b2,carspeed,sensor_infrared,sensor_on
    infrared = 11
    ultrasonic = 8
    servomotor = 7
    motor_L1 = 19
    motor_L2 = 21
    motor_R1 = 24
    motor_R2 = 26
    a1 = GPIO.PWM(motor_L1, 50)
    a2 = GPIO.PWM(motor_L2, 50)
    b1 = GPIO.PWM(motor_R1, 50)
    b2 = GPIO.PWM(motor_R2, 50)
    servo_turning_time = 0.5
    carspeed = 100
    sensor_infrared = False
    sensor_on = True
    #===================================================================================================
    inputpin = [infrared,ultrasonic]
    outputpin = [servomotor,motor_L1,motor_L2,motor_R1,motor_R2]

    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(inputpin,GPIO.IN)
    GPIO.setup(outputpin,GPIO.OUT,initial = GPIO.LOW)


def gpio_end():
    GPIO.cleanup()
    print("all GPIO pin is clean up")


def sensor_if():
    global sensor_infrared
    if GPIO.INPUT(infrared) == 1:
        sensor_infrared = True
    elif GPIO.INPUT(infrared) == 0:
        sensor_infrared = False
    else:
        print("infrared sensor error")
    pass


def sensor_ultrasonic():
    pass


def motor_turn_left():
    p.start(?)
    time.sleep(servo_turning_time)
    p.stop()
    pass


def motor_turn_right():
    p.start(?)
    time.sleep(servo_turning_time)
    p.stop()
    pass


def motor_netural():
    p.start(7)  #dutycycle of netural
    time.sleep(servo_turning_time)
    p.stop()
    pass


def motor_stop():
    p.stop()
    a1.stop()
    a2.stop()
    b1.stop()
    b2.stop()
    GPIO.out(outputpin,GPIO.LOW)
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
    while sensor_on:
        if  sensor_infrared = True:
            a1.stop()
            b1.stop()
            pass

