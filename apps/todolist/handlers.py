# coding: utf-8
from models import Task
from apps.rest import RestHandler, MongoEngineDataManager
from apps.base import TodoListHandler


class Home(TodoListHandler):
    def get(self):
        if self.current_user():
            self.render('tasks/rich.html')
        else:
            self.render('main.html')


class TasksHandler(TodoListHandler):
    def get(self):
        self.render('tasks/rich.html')


class TaskCrudHandler(RestHandler):
    data_manager = MongoEngineDataManager(Task)
