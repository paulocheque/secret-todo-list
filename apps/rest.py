# coding: utf-8
import collections

import simplejson as json
import tornado.web

from utils import to_json


class MongoEngineDataManager(object):
    def __init__(self, model):
        self.model = model

    def read_list(self, initial=0, amount=50):
        return self.model.objects.all()[initial:initial+amount]

    def read(self, identifier):
        try:
            return self.read_list().get(pk=identifier)
        except self.model.DoesNotExist:
            return None

    def create(self, data):
        obj = self.model(**data)
        obj.save()
        return obj

    def update(self, identifier, data):
        obj = self.read(identifier)
        if obj:
            update_query = {}
            for key, value in data.items():
                update_query['set__%s' % key] = value
            obj.update(**update_query)
        return obj

    def delete(self, identifier):
        obj = self.read(identifier)
        if obj:
            obj.delete()
        return obj


class ApiHandler(tornado.web.RequestHandler):
    def answer(self, data):
        self.set_header("Content-Type", "application/json")
        is_iterable = isinstance(data, collections.Iterable) and hasattr(data, '__iter__') and not hasattr(data, 'to_mongo')
        # print(type(data), is_iterable, data)
        if is_iterable:
            data_obj = [dict(d.to_mongo()) if hasattr(d, 'to_mongo') else d for d in data]
        else:
            data_obj = dict(data.to_mongo()) if hasattr(data, 'to_mongo') else data
        data_json = to_json(data_obj)
        self.write(data_json)

    def get_request_data(self):
        data = {}
        for arg in list(self.request.arguments.keys()):
            data[arg] = self.get_argument(arg)
            if data[arg] == '': # Tornado 3.0+ compatibility
                data[arg] = None
            if data[arg] and data[arg].lower() in ['false']:
                data[arg] = False
        return data

    def raise403(self):
        raise tornado.web.HTTPError(403, 'Not enough permissions to perform this action')

    def raise404(self):
        raise tornado.web.HTTPError(404, 'Object not found')


class RestHandler(ApiHandler):
    # CREATE /objs
    def post(self):
        data = self.get_request_data()
        obj = self.data_manager.create(data)
        if obj:
            self.answer(obj)
        else:
            self.answer(obj)

    # LIST /objs/
    # READ /objs/:id
    def get(self, identifier=None):
        if identifier:
            obj = self.data_manager.read(identifier)
            if obj:
                self.answer(obj)
            else:
                self.answer(obj)
        else:
            # FIXME pagination
            initial = int(self.get_argument('initial', default=0))
            amount = int(self.get_argument('amount', default=50))
            objs = self.data_manager.read_list(initial=initial, amount=amount)
            self.answer(objs)

    # UPDATE /objs/:id
    def put(self, identifier):
        data = self.get_request_data()
        obj = self.data_manager.update(identifier, data)
        if obj:
            self.answer(obj)
        else:
            self.answer(obj)

    # DELETE /objs/:id/delete
    def delete(self, identifier):
        obj = self.data_manager.delete(identifier)
        if obj:
            self.answer(obj)
        else:
            self.answer(obj)
