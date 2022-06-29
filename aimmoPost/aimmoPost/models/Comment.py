from mongoengine import *
from .User import User
from .Like import Like
import datetime


class ReComment(Document):
    writer = ReferenceField(User, required=True)
    date = DateTimeField(default=datetime.datetime.utcnow)
    like = ReferenceField(Like)


class Comment(Document):
    writer = ReferenceField(User, required=True)
    date = DateTimeField(default=datetime.datetime.utcnow)
    like = ReferenceField(Like)
    re_comment = ListField(ReferenceField(ReComment), default=list)
