import tornado.web
from tornado.web import RequestHandler
from tornado.websocket import WebSocketHandler
import json


class IndexHandler(RequestHandler):
    def get(self, *args, **kwargs):
        self.xsrf_token


class LoginHandler(RequestHandler):
    def get(self, *args, **kwargs):
        self.render('index/login.html', flag=False, title="登录界面")

    def post(self, *args, **kwargs):
        userId = self.get_body_argument('userId')
        password = self.get_body_argument('password')
        sql = "select * from user where userId='%s' and password='%s'" % (userId, password)
        res = self.application.db.get_all(sql)
        if res:
            loginname = res[0][-1]
            if loginname not in self.application.user:
                self.set_secure_cookie('username', loginname)
                self.redirect('/success')
            else:
                self.render('index/login.html', flag="login", title="登录界面")
        else:
            self.render('index/login.html', flag=True, title="登录界面")


class SuccessHandler(RequestHandler):
    def get_current_user(self):
        return self.get_cookie('username')

    @tornado.web.authenticated
    def get(self, *args, **kwargs):
        username = self.get_secure_cookie('username').decode()
        self.render('index/chat.html', username=username, title="聊天界面")


class QuitHandler(RequestHandler):
    def get(self, *args, **kwargs):
        self.clear_all_cookies()
        self.redirect('/login')


class RegisterHandler(RequestHandler):
    def get(self, *args, **kwargs):
        self.render('index/register.html', title="注册界面")

    def post(self, *args, **kwargs):
        userId = self.get_body_argument('userId')
        username = self.get_body_argument('username')
        password = self.get_body_argument('password')
        sql = "insert into user (userId,username,password) values ('%s','%s','%s')" % (userId, username, password)
        res = self.application.db.insert(sql)
        if res:
            self.render('index/message.html', title='注册成功', href='登录界面', url='/login')
        else:
            self.render('index/message.html', title='注册失败', href='重新注册', url='/register')


class ChatWebSocker(WebSocketHandler):
    users = []

    def open(self, *args, **kwargs):
        self.users.append(self)
        self.username = self.get_secure_cookie("username").decode()
        self.application.user.append(self.username)
        for user in self.users:
            user.write_message(u"<span style='color:green;'>[%s]登陆了</span>" % self.username)

    def on_message(self, message):
        messagelist = message.split("|", 1)
        message = messagelist[-1]
        msguser = messagelist[0]
        userlist = []

        if msguser[-1] == ".":
            msguserlist = msguser[:-1].split(".")
            msguser = msguserlist[0]
            del msguserlist[0]
            if self.username in msguserlist:
                msguserlist.remove(self.username)
            userlist = msguserlist
        for user in self.users:
            if user == self:
                continue
            if len(userlist):
                if user.username in userlist:
                    user.write_message(msguser + r"[%s]：</span>%s" % (self.username, message))
                continue
            user.write_message(msguser + r"[%s]：</span>%s" % (self.username, message))

    def on_close(self):
        self.application.user.remove(self.username)
        self.users.remove(self)
        for user in self.users:
            user.write_message(u"<span style='color:yellow;'>[%s]下线了</span>" % self.username)

    def check_origin(self, origin):
        return True


class CheckHandler(RequestHandler):
    def get(self, *args, **kwargs):
        username = self.get_argument("username", None)
        userId = self.get_argument("userId", None)
        sql = ''
        if username:
            sql = "select * from user where username='%s'" % (username)
        elif userId:
            sql = "select * from user where userId='%s'" % (userId)
        res = self.application.db.get_all(sql)
        res = json.dumps(res)
        self.write(res)


class FlistHandler(RequestHandler):
    def get(self, *args, **kwargs):
        self.username = self.get_secure_cookie("username").decode()
        flist = self.application.user.copy()
        if self.username in flist:
            flist.remove(self.username)
        self.write(json.dumps(flist))
