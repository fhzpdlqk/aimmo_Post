from mongoengine import *
from .User import User


class Like(Document):
    writer = StringField()
