import tornado.web
from views.index import *
import config
import mysqltool
class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r'/index', IndexHandler),
            (r'/login', LoginHandler),
            (r'/success', SuccessHandler),
            (r'/quit', QuitHandler),
            (r'/register', RegisterHandler),
            (r'/chat', ChatWebSocker),
            (r'/check', CheckHandler),
            (r'/flist', FlistHandler),
        ]
        super(Application, self).__init__(handlers,**config.settings)
        self.db = mysqltool.Mysqltool("localhost","root","root","webqq")
        self.user = []