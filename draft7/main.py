import web
from web import form
import socket
import sensor
import RPi.GPIO as GPIO
import time
from threading import Thread
localhost = "http://" + socket.gethostbyname(socket.gethostname()) + ":8080"
print(localhost)
global infrared, ultrasonic, servomotor, motor_L1, motor_L2, motor_R1, motor_R2, servo_turning_time, outputpin, carspeed, sensor_infrared, sensor_on, gpiodidstartup
global move_left,move_right,move_forward,move_backward,sensor_on,move_netural,move_stop,autostop
ultrasonic = 8
infrared = 11
servomotor = 12
motor_L1 = 19
motor_L2 = 21
motor_R1 = 24
motor_R2 = 26
servo_turning_time = 0.5
carspeed = 100
sensor_infrared = False
sensor_on = True
move_left = False
move_right = False
move_netural = False
move_forward = False
move_backward = False
sensor_on = False
move_stop = False
autostop = True
gpiodidstartup = False

urls = (
        '/','Login',
        '/control','Page_one',
        '/left', 'Left',
        '/right', 'Right',
        '/forward', 'Forward',
        '/start', 'Start',
        '/stop', 'Stop',
        '/backward', 'Backward',
        '/about', 'About',
        '/setting','Setting',
        '/updatelog', 'Updatelog',
        '/source_code', 'Sourcecode',
        '/logoff', 'Logoff',
        '/stopserver', 'Stopserver',
        '/result_sensor_ultrasonic', 'Result_sensor_ultrasonic',
)

app = web.application(urls, globals())

loginform = form.Form(
    form.Textbox("USERNAME",
        form.notnull,
        form.Validator('wrong', lambda x: x == "martin")),
    form.Textbox("PASSWORD",
        form.notnull,
        form.Validator('wrong', lambda x: x == "12341234")),
    form.Checkbox('I am not a robot'))

render = web.template.render('templates/')


class Login:
        def GET(self):
            return render.login(loginform)

        def POST(self):
            if not loginform.validates():
                return render.login(loginform)
            else:
                gpio_startup()
                return web.seeother('/control')


class Page_one:
        def GET(self):
            return render.page_one()

        def POST(self):
            return render.page_one()


class Left:
    def GET(self):
        move_left = True
        move_right = False
        move_netural = False
        move_forward = False
        move_backward = False
        move_stop = False
        autostop = False
        print("left")
        return "left"


class Right:
    def GET(self):
        move_left = False
        move_right = True
        move_netural = False
        move_forward = False
        move_backward = False
        move_stop = False
        autostop = False
        print("right")
        return "right"


class Forward:
    def GET(self):
        move_left = False
        move_right = False
        move_netural = True
        move_forward = True
        move_backward = False
        move_stop = False
        autostop = False
        print("forward")
        return "forward"


class Start:
    def GET(self):
        move_left = False
        move_right = False
        move_netural = False
        move_forward = False
        move_backward = False
        move_stop = False
        autostop = False
        print("start")
        return "start"


class Backward:
    def GET(self):
        move_left = False
        move_right = False
        move_netural = True
        move_forward = False
        move_backward = True
        move_stop = False
        autostop = False
        print("backward")
        return "backward"


class Stop:
    def GET(self):
        move_left = False
        move_right = False
        move_netural = False
        move_forward = False
        move_backward = False
        move_stop = False
        autostop = False
        print("stop")
        return "stop"


class About:
    def GET(self):
        move_left = False
        move_right = False
        move_netural = False
        move_forward = False
        move_backward = False
        move_stop = False
        autostop = False
        return render.about()


class Setting:
    def GET(self):
        move_left = False
        move_right = False
        move_netural = False
        move_forward = False
        move_backward = False
        move_stop = False
        autostop = False
        return render.setting()


class Updatelog:
    def GET(self):
        move_left = False
        move_right = False
        move_netural = False
        move_forward = False
        move_backward = False
        move_stop = False
        autostop = False
        return render.updatelog()


class Sourcecode:
    def GET(self):
        move_left = False
        move_right = False
        move_netural = False
        move_forward = False
        move_backward = False
        move_stop = False
        autostop = False
        return render.source_code()


class Logoff:
    def GET(self):
        global gpiodidstartup
        move_left = False
        move_right = False
        move_netural = False
        move_forward = False
        move_backward = False
        move_stop = False
        autostop = False
        gpio_end()
        gpiodidstartup = False
        return render.logoff()


class Stopserver:
    def GET(self):
        move_left = False
        move_right = False
        move_netural = False
        move_forward = False
        move_backward = False
        move_stop = False
        autostop = False
        return exit()


class Result_sensor_ultrasonic:
    def GET(self):
        return sensor_ultrasonic()

def motormovement():
    while True:
        while gpiodidstartup:
            t1 = Thread(target=motor_turn_left)
            t2 = Thread(target=motor_turn_right)
            t3 = Thread(target=motor_netural)
            t4 = Thread(target=motor_stop)
            t5 = Thread(target=motor_forward)
            t6 = Thread(target=motor_backward)
            t7 = Thread(target=collision_prevention_system)
            t1.daemon = True
            t2.daemon = True
            t3.daemon = True
            t4.daemon = True
            t5.daemon = True
            t6.daemon = True
            t7.daemon = True
            t1.start()
            t2.start()
            t3.start()
            t4.start()
            t5.start()
            t6.start()
            t7.start()
            return


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
    while move_left:
        p.start(5)
        time.sleep(servo_turning_time)
        p.stop()


def motor_turn_right():
    while move_right:
        p.start(10)
        time.sleep(servo_turning_time)
        p.stop()


def motor_netural():
    while move_netural:
        p.start(7.5)  #dutycycle of netural
        time.sleep(servo_turning_time)
        p.stop()



def motor_stop():
    while move_stop:
        p.stop()
        a1.stop()
        a2.stop()
        b1.stop()
        b2.stop()



def motor_forward(carspeed = carspeed):
    while move_forward:
        a1.start(0)
        b1.start(0)
        a1.start(carspeed)
        b1.start(carspeed)



def motor_backward(carspeed = carspeed):
    while move_backward:
        a2.start(0)
        b2.start(0)
        a2.start(carspeed)
        b2.start(carspeed)


def change_speed(direction,speed):  #1 for forward 2 for backward, anyother number will result in error
    carspeed = speed
    if direction == 1:
        motor_forward(carspeed)
    elif direction == 2:
        motor_backward(carspeed)
    else:
        print('Direction error')


def collision_prevention_system():
    while autostop:
        if detect_distance < 10:
            a1.stop()
            b1.stop()
            a2.stop()
            b2.stop()


if __name__ == "__main__" :
    motor = Thread(target=motormovement)
    motor.daemon = True
    motor.start()
    app.run()