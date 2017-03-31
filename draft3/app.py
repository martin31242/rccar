import web
import random

urls = (
    '/', 'rand_num',
    '/random','return_num')

render = web.template.render('templates/')


class rand_num:
    def GET(self):
        return render.random()

class return_num:
    def GET(self):
        print("test")
        return "123"#random.randint(1,1000)

if __name__ == "__main__":
    app = web.application(urls, globals(), True)
    app.run()