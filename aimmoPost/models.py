from mongoengine import *
from . import config


class User(Document):
    _id = StringField(required="True", max_length=200, primary_key=True)
    pw = StringField(required="True", max_length=100)
