# coding: utf-8
from apps.utils.rest import *
from apps.utils.base import *
from .models import *


class HomeHandler(BaseHandler):
    def get(self):
        if self.get_current_user():
            self.render('todolist/todolists.html')
        else:
            self.render('todolist/main.html', alert='You have to login first')


class TodoListsHandler(AuthenticatedBaseHandler):
    def get(self):
        self.render('todolist/todolists.html')


class TasksHandler(AuthenticatedBaseHandler):
    def get(self, todolist_id):
        self.render('todolist/tasks.html', todolist_id=todolist_id)


class TodoListCrudHandler(RestHandler):
    model = TodoList
    user_mapping_path = 'user'
    perm_public = ''
    perm_user = 'CRLUD'
    perm_admin = 'CRLUD'


class TaskDataManager(MongoEngineDataManager):
    def read_list(self, initial=0, amount=50, data=None):
        objs = super(TaskDataManager, self).read_list(initial=initial, amount=amount, data=data)
        todolist = data.get('todolist')
        objs = objs.filter(todolist=todolist)
        return objs


class TaskCrudHandler(RestHandler):
    model = Task
    data_manager = TaskDataManager
    dependencies = [TodoList]
    user_mapping_path = 'todolist.user'
    perm_public = ''
    perm_user = 'CRLUD'
    perm_admin = 'CRLUD'

