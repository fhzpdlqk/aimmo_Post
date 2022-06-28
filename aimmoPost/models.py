from mongoengine import *
from . import config


class User(Document):
    user_id = StringField(required="True", max_length=200)
    user_pw = StringField(required="True", max_length=100)
