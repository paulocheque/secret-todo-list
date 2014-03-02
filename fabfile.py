# coding: utf-8
import sys
sys.path.append('.')

import logging
logging.getLogger().setLevel(logging.INFO)

from fabric.api import task

import connect_mongo
from apps.system_settings.models import *
from apps.accounts.models import *
from apps.todolist.models import *
# from apps.todolist.tasks import *


# https://gist.github.com/paulocheque/5906909
def colorize(message, color='blue'):
    color_codes = dict(black=30, red=31, green=32, yellow=33, blue=34, magenta=35, cyan=36, white=37)
    code = color_codes.get(color, 34)
    msg = '\033[%(code)sm%(message)s\033[0m' % {'code':code, 'message':message}
    # print(msg)
    return msg


@task
def report():
    print(colorize('=' * 80))
    print(colorize('Report'))
    print(colorize('=' * 80))
    print(colorize('Settings', color='cyan'))
    ss = SystemSettings.get()
    for k, v in vars(ss)['_data'].items():
        if k != 'singleton' and k != 'id':
            print('%s: %s' % (k, v))
    print('-' * 50)
    print('%s users' % User.objects.count())
    print('-' * 50)
    print('%s todolists' % TodoList.objects.count())
    print('%s tasks' % Task.objects.count())
    print('%s completed tasks' % Task.objects(completed=True).count())
