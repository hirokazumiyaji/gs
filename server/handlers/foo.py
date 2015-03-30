import tornado.web


class FooHandler(tornado.web.RequestHandler):

    def get(self):
        self.write('Hello world!')
        self.finish()
