from mongoengine import *
from .User import User


class Like(Document):
    writer_list = ListField(StringField, default=list)
