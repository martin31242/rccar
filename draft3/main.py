import web
from web import form
import socket
print("http://" + socket.gethostbyname(socket.gethostname()) + ":8080")

urls = (
        '/','Login',
        '/page_one','Page_one',
        '/left', 'Left',
        '/right', 'Right',
        '/forward', 'Forward',
        '/start', 'Start',
        '/stop', 'Stop',
        '/backward', 'Backward',
        '/about', 'About',
        '','',
        '', '',
        '', '',
        '', '',
        '', '',
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
                session.logged_in = True
                return web.seeother('/page_one')

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
        print("stop")
        return "stop"






if __name__ == "__main__" :
    app.run()
