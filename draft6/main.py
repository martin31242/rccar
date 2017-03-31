import web
from web import form
import socket
import sensor
from threading import Thread
localhost = "http://" + socket.gethostbyname(socket.gethostname()) + ":8080"
print(localhost)

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
                sensor.gpio_startup()
                return web.seeother('/control')


class Page_one:
        def GET(self):
            return render.page_one()

        def POST(self):
            return render.page_one()


class Left:
    def GET(self):
        sensor.move_left = True
        sensor.move_right = False
        sensor.move_netural = False
        sensor.move_forward = False
        sensor.move_backward = False
        sensor.move_stop = False
        sensor.autostop = False
        print("left")
        return "left"


class Right:
    def GET(self):
        sensor.move_left = False
        sensor.move_right = True
        sensor.move_netural = False
        sensor.move_forward = False
        sensor.move_backward = False
        sensor.move_stop = False
        sensor.autostop = False
        print("right")
        return "right"


class Forward:
    def GET(self):
        sensor.move_left = False
        sensor.move_right = False
        sensor.move_netural = True
        sensor.move_forward = True
        sensor.move_backward = False
        sensor.move_stop = False
        sensor.autostop = False
        print("forward")
        return "forward"


class Start:
    def GET(self):
        sensor.move_left = False
        sensor.move_right = False
        sensor.move_netural = False
        sensor.move_forward = False
        sensor.move_backward = False
        sensor.move_stop = False
        sensor.autostop = False
        print("start")
        return "start"


class Backward:
    def GET(self):
        sensor.move_left = False
        sensor.move_right = False
        sensor.move_netural = True
        sensor.move_forward = False
        sensor.move_backward = True
        sensor.move_stop = False
        sensor.autostop = False
        print("backward")
        return "backward"


class Stop:
    def GET(self):
        sensor.move_left = False
        sensor.move_right = False
        sensor.move_netural = False
        sensor.move_forward = False
        sensor.move_backward = False
        sensor.move_stop = False
        sensor.autostop = False
        print("stop")
        return "stop"


class About:
    def GET(self):
        sensor.move_left = False
        sensor.move_right = False
        sensor.move_netural = False
        sensor.move_forward = False
        sensor.move_backward = False
        sensor.move_stop = False
        sensor.autostop = False
        return render.about()


class Setting:
    def GET(self):
        sensor.move_left = False
        sensor.move_right = False
        sensor.move_netural = False
        sensor.move_forward = False
        sensor.move_backward = False
        sensor.move_stop = False
        sensor.autostop = False
        return render.setting()


class Updatelog:
    def GET(self):
        sensor.move_left = False
        sensor.move_right = False
        sensor.move_netural = False
        sensor.move_forward = False
        sensor.move_backward = False
        sensor.move_stop = False
        sensor.autostop = False
        return render.updatelog()


class Sourcecode:
    def GET(self):
        sensor.move_left = False
        sensor.move_right = False
        sensor.move_netural = False
        sensor.move_forward = False
        sensor.move_backward = False
        sensor.move_stop = False
        sensor.autostop = False
        return render.source_code()


class Logoff:
    def GET(self):
        global gpiodidstartup
        sensor.move_left = False
        sensor.move_right = False
        sensor.move_netural = False
        sensor.move_forward = False
        sensor.move_backward = False
        sensor.move_stop = False
        sensor.autostop = False
        sensor.gpio_end()
        gpiodidstartup = False
        return render.logoff()


class Stopserver:
    def GET(self):
        sensor.move_left = False
        sensor.move_right = False
        sensor.move_netural = False
        sensor.move_forward = False
        sensor.move_backward = False
        sensor.move_stop = False
        sensor.autostop = False
        return exit()


class Result_sensor_ultrasonic:
    def GET(self):
        return sensor.sensor_ultrasonic()

def motormovement():
    while True:
        while sensor.gpiodidstartup:
            t1 = Thread(target=sensor.motor_turn_left)
            t2 = Thread(target=sensor.motor_turn_right)
            t3 = Thread(target=sensor.motor_netural)
            t4 = Thread(target=sensor.motor_stop)
            t5 = Thread(target=sensor.motor_forward)
            t6 = Thread(target=sensor.motor_backward)
            t7 = Thread(target=sensor.collision_prevention_system)
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
    
if __name__ == "__main__" :
    global temp_variable
    temp_variable = True
    motor = Thread(target=motormovement)
    motor.daemon = True
    motor.start()
    app.run()