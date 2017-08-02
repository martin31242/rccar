import web,socket,time,Adafruit_ADS1x15,tempvar
from web import form
import RPi.GPIO as GPIO
from threading import Thread
localhost = "http://" + socket.gethostbyname(socket.gethostname()) + ":8080"
print(localhost)
#global infrared, ultrasonic, servomotor, motor_L1, motor_L2, motor_R1, motor_R2, servo_turning_time, outputpin, carspeed, gpiodidstartup

ultrasonic = 8
infrared = 7
servomotor = 12
motor_L1 = 19
motor_L2 = 21
motor_R1 = 24
motor_R2 = 26
servo_turning_time = 1
carspeed = 100
gpiodidstartup = False
servomotor_camera = 13
light_signal_ready =
light_red =
light_yellow_left =
light_yellow_right =
light_green =


adc = Adafruit_ADS1x15.ADS1115()


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
        '/route','Route',
        '/stopserver', 'Stopserver',
        '/result_sensor_ultrasonic', 'Result_sensor_ultrasonic',
        '/result_sensor_infrared','Result_sensor_infrared',
        '/toggle_ultrasonic','Toggle_ultrasonic',
        '/toggle_infrared','Toggle_infrared',
        '/camera/(.*)','Camera_angle',
       # '/','',
     #   '/','',
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
    form.Checkbox('I am not a robot')
)

routeform = form.Form(

)

render = web.template.render('templates/')

def gpio_startup():
    global a1,a2,b1,b2,gpiodidstartup,p,servomotor_camera,p1
    GPIO.setmode(GPIO.BOARD)
    inputpin = [infrared,ultrasonic]
    outputpin = [servomotor,motor_L1,motor_L2,motor_R1,motor_R2,servomotor_camera,light_red,light_yellow_left,light_yellow_right,light_green,light_signal_ready]
    GPIO.setup(inputpin,GPIO.IN)
    GPIO.setup(outputpin,GPIO.OUT,initial = GPIO.LOW)
    a1 = GPIO.PWM(motor_L1, 50)
    a2 = GPIO.PWM(motor_L2, 50)
    b1 = GPIO.PWM(motor_R1, 50)
    b2 = GPIO.PWM(motor_R2, 50)
    gpiodidstartup = True
    p = GPIO.PWM(servomotor,50)
    p1 = GPIO.PWM(servomotor_camera,50)
    p.start(0)
    p1.start(0)
    a1.start(0)
    a2.start(0)
    b1.start(0)
    b2.start(0)


def gpio_end():
    GPIO.cleanup()
    print("all GPIO pin is clean up")


def sensor_infrared():
    tempvar.count_time_logoff = 0
    tempvar.count_time_stop_if_not_responding = 0
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
        p.ChangeDutyCycle(5)
        time.sleep(servo_turning_time)


def motor_turn_right():
        p.ChangeDutyCycle(10)
        time.sleep(servo_turning_time)


def motor_netural():
        p.ChangeDutyCycle(7.5)
        time.sleep(servo_turning_time)


def motor_stop():
        a1.ChangeDutyCycle(0)
        a2.ChangeDutyCycle(0)
        b1.ChangeDutyCycle(0)
        b2.ChangeDutyCycle(0)


def motor_forward(carspeed = carspeed):
        a1.ChangeDutyCycle(carspeed)
        b1.ChangeDutyCycle(carspeed)


def motor_backward(carspeed = carspeed):
        a2.ChangeDutyCycle(carspeed)
        b2.ChangeDutyCycle(carspeed)


def collision_prevention_system():
        if detect_distance < 10:
            a1.ChangeDutyCycle(0)
            b1.ChangeDutyCycle(0)
            a2.ChangeDutyCycle(0)
            b2.ChangeDutyCycle(0)


def auto_logoff():
    while tempvar.count_time_logoff < 600:
        tempvar.count_time_logoff += 1
        print(tempvar.count_time_logoff)
        time.sleep(1)
    return web.seeother('/stopserver')


def notresponding():
    while True:
        while tempvar.count_time_stop_if_not_responding < 5:
            tempvar.count_time_stop_if_not_responding += 1
            print(tempvar.count_time_stop_if_not_responding)
            time.sleep(1)
        motor_stop()
        time.sleep(5)


def servo_motor_left():
    p1.ChangeDutyCycle(5)


def servo_motor_center():
    p1.ChangeDutyCycle(7.5)


def servo_motor_right():
    p1.ChangeDutyCycle(10)


def ready_error_signal_on():
    GPIO.output(light_signal_ready,GPIO.HIGH)


def ready_error_signal_off():
    GPIO.output(light_signal_ready, GPIO.LOW)


class Login:
        def GET(self):
            return render.login(loginform)

        def POST(self):
            if not loginform.validates():
                return render.login(loginform)
            else:
                gpio_startup()
                tt1 = Thread(target=auto_logoff)
                tt2 = Thread(target=notresponding)
                tt1.daemon = True
                tt2.daemon = True
                tt1.start()
                tt2.start()
                return web.seeother('/control')


class Page_one:
        def GET(self):
            tt2 = Thread(target=notresponding)
            tt2.daemon = True
            tt2.start()
            servo_motor_center()
            motor_netural()
            ready_error_signal_on()
            return render.page_one()

        def POST(self):
            return render.page_one()


class Left:
    def GET(self):
        motor_turn_left()
        #print("left")
        return "left"


class Right:
    def GET(self):
        motor_turn_right()
        #print("right")
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
        #print("forward")
        return "forward"


class Start:
    def GET(self):
        #print("start")
        return "start"


class Backward:
    def GET(self):
        motor_stop()
        motor_backward()
        #print("backward")
        return "backward"


class Stop:
    def GET(self):
        motor_stop()
        #print("stop")
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

class Route:
    def GET(self):
        return render.route()

    def POST(self):
        i = web.input()
        asd = i.message
        words = asd.split()
        print(words)
        for i in words:
            if i == u'Forward':# u' stand for encode in unicode, when return data from the web it is encode in unicode
                motor_forward()
                time.sleep(1)
            elif i == u'Left':
                motor_turn_left()
                time.sleep(1)
            elif i == u'Right':
                motor_turn_right()
                time.sleep(1)
            elif i == u'Backward':
                motor_backward()
                time.sleep(1)
            elif i == u'Stop':
                motor_stop()
                time.sleep(1)
            else:
                pass
        motor_stop()
        return render.route()

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


class Camera_angle:
    def GET(self, count):
        if count == '90':
            servo_motor_center()
            return "Center"
        elif count == '60':
            servo_motor_right()
            return "right"
        elif count == '120'':
            servo_motor_left()
            return "Left"

if __name__ == "__main__" :
    app.run()