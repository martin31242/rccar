import web
from web import form
import socket
import sensor
import time
From threading import Thread
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
        '', '',
        '', '',
        '', '',




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
                sensor.gpio_startup()p
                return web.seeother('/control')

class Page_one:
        def GET(self):

            return render.page_one()


        def POST(self):
            return render.page_one()

class return_num:
    def GET(self):
        print("test")
        return "123"

class Left:
    def GET(self):
        print("left")
        return "left"

class Right:
    def GET(self):
        print("right")
        return "right"

class Forward:
    def GET(self):
        sensor.motor_netural()
        sensor.motor_forward()
        print("forward")
        return "forward"

class Start:
    def GET(self):
        print("start")
        return "start"

class Backward:
    def GET(self):
        print("backward")
        return "backward"

class Stop:
    def GET(self):
        sensor.motor_stop()
        print("stop")
        return "stop"

class About:
    def GET(self):
        return render.about()

class Setting:
    def GET(self):
        return render.setting()

class Updatelog:
    def GET(self):
        return render.updatelog()

class Sourcecode:
    def GET(self):
        return render.source_code()

class Logoff:
    def GET(self):
        sensor.gpio_end()
        return render.logoff()

class Stopserver:
    def GET(self):
        return exit()

if __name__ == "__main__" :
    t1 = thread(target = app.run())
    t2 = thread(target = sensor.collision_prevention_system())
    t1.start()
    t2.start()
