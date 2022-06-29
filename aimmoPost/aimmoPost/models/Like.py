from mongoengine import *
from . import User


class Like(Document):
    num = IntField(default=0)
    writer_list = ListField(ReferenceField(User))
