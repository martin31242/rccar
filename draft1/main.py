import web
from web import form
import socket
print("http://" + socket.gethostbyname(socket.gethostname()) + ":8080")

urls = (
        '/index', 'Index',
        '/','Login',
        '/page_one','Page_one'
)
loginform = form.Form(
    form.Textbox("USERNAME",
        form.notnull,
        form.Validator('wrong', lambda x: x == "martin")),
    form.Textbox("PASSWORD",
        form.notnull,
        form.Validator('wrong', lambda x: x == "12341234")),
    form.Checkbox('I am not a robot'))

left_form = form.Form(form.Button("left", value="left", id="left", style="height:30px;width:80px" ))
foward_form = form.Form(form.Button("foward", value="foward", style="height:30px;width:80px"))
backward_form = form.Form(form.Button("backward", value="backward", style="height:30px;width:80px"))
right_form = form.Form(form.Button("right", value="right", style="height:30px;width:80px"))
start_form = form.Form(form.Button("start", value="start", style="height:30px;width:80px"))
stop_form = form.Form(form.Button("stop", value="stop", style="height:30px;width:80px"))

render = web.template.render('template/')

class Index:
        def GET(self):
            left = left_form
            right = right_form
            foward = foward_form
            backward = backward_form
            start = start_form
            stop = stop_form
            return render.index(form,left,right,foward,backward,start,stop)
        def POST(self):
            left = left_form
            right = right_form
            foward = foward_form
            backward = backward_form
            start = start_form
            stop = stop_form
            userData = web.data()
            print(userData)
            if userData == "backward=backward":
                pass
            elif userData == "left=left":
                pass
            elif userData == "right=right":
                pass
            elif userData == "foward=foward":
                pass
            elif userData == "stop=stop":
                pass
            elif userData == "left=left":
                pass
            elif userData == "gotopagone":
                return web.seeother('/page_one')
            return render.index(form,left,right,foward,backward,start,stop)


class Login:
        def GET(self):
            form = loginform()
            return render.login(form)

        def POST(self):
            form = loginform()
            if not form.validates():
                return render.login(form)
            else:
                return web.seeother('/page_one')

class Page_one:
        def GET(self):
            left = left_form
            right = right_form
            foward = foward_form
            backward = backward_form
            start = start_form
            stop = stop_form
            return render.page_one(form,left,right,foward,backward,start,stop)
            pass

        def POST(self):
            left = left_form
            right = right_form
            foward = foward_form
            backward = backward_form
            start = start_form
            stop = stop_form
            userData=web.data()
            print(userData)
            return render.page_one(form,left,right,foward,backward,start,stop)
            pass


if __name__ == "__main__" :
    app = web.application(urls, globals())
    app.run()
