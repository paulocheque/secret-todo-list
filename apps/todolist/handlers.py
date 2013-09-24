# coding: utf-8
from models import TodoList, Task
from apps.rest import RestHandler, MongoEngineDataManagerPerUser
from apps.complex_rest import ComplexRestHandler, MongoEngineComplexDataManagerPerUser
from apps.base import TodoListHandler


class Home(TodoListHandler):
    def get(self):
        if self.get_current_user():
            self.render('todolist/todolists.html')
        else:
            self.render('main.html')


class TodoListsHandler(TodoListHandler):
    def get(self):
        if self.get_current_user():
            self.render('todolist/todolists.html')
        else:
            self.render('main.html')


class TasksHandler(TodoListHandler):
    def get(self, todolist_id):
        if self.get_current_user():
            self.render('todolist/tasks.html', todolist_id=todolist_id)
        else:
            self.render('main.html')


class TodoListCrudHandler(RestHandler):
    def prepare(self):
        super(TodoListCrudHandler, self).prepare()
        self.data_manager = MongoEngineDataManagerPerUser(TodoList, self.get_current_user())


class TaskCrudHandler(ComplexRestHandler):
    def prepare(self):
        super(TaskCrudHandler, self).prepare()
        self.data_manager = MongoEngineComplexDataManagerPerUser(Task, [TodoList], self.get_current_user(),
            user_filter_path='todolist__user')
