import web
from web import form
import socket
import sensor
import time
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
        sensor.move_left = False
        sensor.move_right = False
        sensor.move_netural = False
        sensor.move_forward = False
        sensor.move_backward = False
        sensor.move_stop = False
        sensor.autostop = False
        sensor.gpio_end()
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

    
if __name__ == "__main__" :
    sensor.t7.start()
    app.run()