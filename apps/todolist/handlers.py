# coding: utf-8
from models import Task
from apps.rest import RestHandler, MongoEngineDataManagerPerUser
from apps.base import TodoListHandler


class Home(TodoListHandler):
    def get(self):
        if self.get_current_user():
            self.render('tasks/rich.html')
        else:
            self.render('main.html')


class TasksHandler(TodoListHandler):
    def get(self):
        if self.get_current_user():
            self.render('tasks/rich.html')
        else:
            self.render('main.html')


class TaskCrudHandler(RestHandler):
    def prepare(self):
        super(TaskCrudHandler, self).prepare()
        self.data_manager = MongoEngineDataManagerPerUser(Task, self.get_current_user())
