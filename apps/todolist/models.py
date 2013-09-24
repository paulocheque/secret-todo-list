# coding: utf-8
from dateutil.parser import parse
from mongoengine import *

from apps.accounts.models import User


class TodoList(Document):
    user = ReferenceField(User, required=True)
    name = StringField(required=True)


class Task(Document):
    todolist = ReferenceField(TodoList, required=True)
    description = StringField(required=True)
    priority = IntField(required=False, default=2, choices=[1, 2, 3])
    due_date = DateTimeField(required=False)
    completed = BooleanField(required=False)

    def save(self, *args, **kwargs):
        if isinstance(self.due_date, str):
            self.due_date = parse(self.due_date, yearfirst=True, dayfirst=True, ignoretz=True)
        return super(Task, self).save(*args, **kwargs)