# coding: utf-8
try:
    import simplejson as json
except ImportError:
    import json
# http://www.tornadoweb.org/documentation/escape.html
# tornado.escape.json_encode(value)[source]
from datetime import date, time
from bson.objectid import ObjectId


class Serializable(object):
    def __init__(self, *args, **kwargs):
        self.__dict__.update(kwargs)


# https://github.com/facebook/tornado/blob/master/tornado/util.py
class ObjectDict(dict):
    '''Makes a dictionary behave like an object, with attribute-style access.'''
    def __getattr__(self, name):
        try:
            return self[name]
        except KeyError:
            raise AttributeError(name)

    def __setattr__(self, name, value):
        self[name] = value


class DefaultEncoder(json.JSONEncoder):
    def __init__(self, date_format='%Y/%m/%d', time_format='%H:%M', **kwargs): # FIXME: numero de segundos e tal
        super(DefaultEncoder, self).__init__(**kwargs)
        self.date_format = date_format
        self.time_format = time_format

    def default(self, obj):
        if isinstance(obj, ObjectId):
            return str(obj)
        if isinstance(obj, date):
            return obj.strftime(self.date_format)
        if isinstance(obj, time):
            return obj.strftime(self.time_format)
        if isinstance(obj, type):
            return obj.__dict__
        return json.JSONEncoder.default(self, obj)


class DefaultDecoder(json.JSONDecoder):
    def __init__(self, date_format='%Y/%m/%d', time_format='%H:%M', **kwargs): # FIXME: numero de segundos e tal
        super(DefaultDecoder, self).__init__(**kwargs)
        self.date_format = date_format
        self.time_format = time_format

    def decode(self, string):
        # print string.__class__
        # if isinstance(obj, dict):
        #     return obj.__dict__
        return super(DefaultDecoder, self).decode(string)


def to_json(dicts, properties=None, encoder_class=DefaultEncoder):
    return json.dumps(dicts, cls=encoder_class)


def from_json(dicts, properties=None, encoder_class=DefaultDecoder):
    return json.loads(dicts, cls=encoder_class)


def to_dict(obj, properties=None, exclude=[]):
    if properties:
        d = vars(obj)
        result = {}
        for prop in properties:
            if prop in result.keys():
                result[prop] = d[prop]
    else:
        result = vars(obj)
    for prop in exclude:
        result.pop(prop, None)

    # for key, prop in result.iteritems():
    #     if not isinstance(prop, (str, unicode, list, set, dict, int, float)):
    #         print '::', key, prop
    return result

