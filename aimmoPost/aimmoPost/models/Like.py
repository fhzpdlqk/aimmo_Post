from mongoengine import *
from .User import User


class Like(Document):
    num = IntField(default=0)
    writer_list = ListField(ReferenceField(User), default=list)
