import web,socket,time,Adafruit_ADS1x15,tempvar
from web import form
import RPi.GPIO as GPIO
from threading import Thread
import threading
localhost = "http://" + socket.gethostbyname(socket.gethostname()) + ":8080"
print(localhost)
global infrared, ultrasonic, servomotor, motor_L1, motor_L2, motor_R1, motor_R2, servo_turning_time, outputpin, carspeed, gpiodidstartup
ultrasonic = 8
infrared = 11
servomotor = 12
motor_L1 = 19
motor_L2 = 21
motor_R1 = 24
motor_R2 = 26
servo_turning_time = 1
carspeed = 100
gpiodidstartup = False
adc = Adafruit_ADS1x15.ADS1115()
lock = threading.lock()


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
        '/setting', 'Setting',
        '/updatelog', 'Updatelog',
        '/source_code', 'Sourcecode',
        '/logoff', 'Logoff',
        '/route','Route'
        '/stopserver', 'Stopserver',
        '/result_sensor_ultrasonic', 'Result_sensor_ultrasonic',
        '/result_sensor_infrared','Result_sensor_infrared',
        '/toggle_ultrasonic','Toggle_ultrasonic',
        '/toggle_infrared','Toggle_infrared',
        '/(.*)','Error_page'
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


def sensor_infrared():
    global lock
    lock.acquire
    tempvar.count_time_logoff = 0
    tempvar.count_time_stop_if_not_responding = 0
    lock.release()
    if tempvar.sensor_status_infrared:
        GAIN = 1
        values = adc.read_adc(0, gain=GAIN)
        values = values / 250
        if values > 95:
            motor_stop()
        return values
    else:
        return "N/A"


def sensor_ultrasonic():
    if tempvar.sensor_status_ultrasonic:
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
        if detect_distance < 5:
            motor_stop()
        return detect_distance
    else:
        return "N/A"


def motor_turn_left():
        p.start(0)
        p.ChangeDutyCycle(5)
        time.sleep(servo_turning_time)
        p.start(0)


def motor_turn_right():
        p.start(0)
        p.ChangeDutyCycle(10)
        time.sleep(servo_turning_time)
        p.start(0)


def motor_netural():
        p.start(0)
        p.ChangeDutyCycle(7.5)
        time.sleep(servo_turning_time)
        p.start(0)



def motor_stop():
        a1.stop()
        a2.stop()
        b1.stop()
        b2.stop()


def motor_forward(carspeed = carspeed):
        a1.start(carspeed)
        b1.start(carspeed)


def motor_backward(carspeed = carspeed):
        a2.start(carspeed)
        b2.start(carspeed)


def collision_prevention_system():
        if detect_distance < 10:
            a1.stop()
            b1.stop()
            a2.stop()
            b2.stop()


def auto_logoff():
    global lock
    while tempvar.count_time_logoff < 600
        lock.acquire
        tempvar.count_time_logoff += 1
        lock.release()
        print(tempvar.count_time_logoff)
        time.sleep(1)


def notresponding():
    global lock
    while tempvar.count_time_stop_if_not_responding < 5
        lock.acquire
        tempvar.count_time_stop_if_not_responding += 1
        lock.release()
        print(tempvar.count_time_stop_if_not_responding)
        time.sleep(1)


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
        motor_turn_left()
        print("left")
        return "left"


class Right:
    def GET(self):
        motor_turn_right()
        print("right")
        return "right"


class Forward:
    def GET(self):
        motor_stop()
        t3 = Thread(target=motor_netural)
        t5 = Thread(target=motor_forward)
        t3.daemon = True
        t5.daemon = True
        t3.start()
        t5.start()
        t3.join()
        t5.join()
        print("forward")
        return "forward"


class Start:
    def GET(self):
        print("start")
        return "start"


class Backward:
    def GET(self):
        motor_stop()
        motor_backward()
        print("backward")
        return "backward"


class Stop:
    def GET(self):
        motor_stop()
        print("stop")
        return "stop"


class About:
    def GET(self):
        motor_stop()
        return render.about()


class Setting:
    def GET(self):
        motor_stop()
        return render.setting()


class Updatelog:
    def GET(self):
        motor_stop()
        return render.updatelog()


class Sourcecode:
    def GET(self):
        motor_stop()
        return render.source_code()


class Logoff:
    def GET(self):
        motor_stop()
        gpio_end()
        return render.logoff()


class Stopserver:
    def GET(self):
        motor_stop()
        return exit()


class Error_page:
    def GET(self):
        return render.pageerror()


class Result_sensor_ultrasonic:
    def GET(self,*args):
        return sensor_ultrasonic()


class Result_sensor_infrared:
    def GET(self,*args):
        return sensor_infrared()

class Toggle_ultrasonic:
    def GET(self):
        if tempvar.sensor_status_ultrasonic:
            tempvar.sensor_status_ultrasonic = False
        else:
            tempvar.sensor_status_ultrasonic = True


class Toggle_infrared:
    def GET(self):
        if tempvar.sensor_status_infrared:
            tempvar.sensor_status_infrared = False
        else:
            tempvar.sensor_status_infrared = True


if __name__ == "__main__" :
    tt1=thread(target=auto_logoff)
    tt2=thread(target=notresponding)
    tt1.daemon = True
    tt2.daemon = True
    tt1.start()
    tt2.start()
    app.run()