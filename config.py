import os
BASE_PATH = os.path.dirname(__file__)
options = {
    'port': 8000,
}

# app配置
settings = {
    'template_path': os.path.join(BASE_PATH,'templates'),
    'static_path': os.path.join(BASE_PATH, 'static/index'),
    'debug': True,
    'cookie_secret': 'bGwHDEmXT8amax9YhA9kYdOdj7fMKEz5lODcbXQ3RAc=',
    # 'xsrf_cookies':True,
    'login_url': '/login',
}