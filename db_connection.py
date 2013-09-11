# coding: utf-8
import os
from mongoengine import *


mongo_url = os.environ.get('MONGOHQ_URL', None)
if mongo_url:
    connect('default', host=mongo_url)
else:
    connect('default')
