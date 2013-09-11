# coding: utf-8
import logging
import os
import sys

import tornado.ioloop
import tornado.web

from settings import *
import db_connection # connect to databases
from tornado_rest_handler import routes, rest_routes

# apps
from apps.home import Home
from apps.accounts.handlers import *

from apps.todolist.models import *
from apps.todolist.handlers import *


logging.basicConfig(
    stream=sys.stdout,
    level=logging.DEBUG,
    format='%(asctime)s %(levelname)8s %(name)s - %(message)s',
    datefmt='%H:%M:%S'
)

TORNADO_ROUTES = [
    (r'/?', Home),

    (r'/register', RegisterHandler),
    (r'/login', LoginHandler),
    (r'/logout', LogoutHandler),
    (r'/change_password', ResetPasswordHandler),
    (r'/account', UserPageHandler),

    (r'/tasks', TasksHandler),
    (r'/api/tasks', TaskCrudHandler),
    (r'/api/tasks/([0-9a-fA-F]{24,})', TaskCrudHandler),
    (r'/api/tasks/([0-9a-fA-F]{24,})/delete', TaskCrudHandler),
]

application = tornado.web.Application(routes(TORNADO_ROUTES), **TORNADO_SETTINGS)


if __name__ == '__main__':
    # http://www.tornadoweb.org/documentation/wsgi.html
    # to use with newrelic
    import newrelic.agent
    application = newrelic.agent.wsgi_application()(application)

    application.listen(5000)
    tornado.ioloop.IOLoop.instance().start()
