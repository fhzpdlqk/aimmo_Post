from mongoengine import *
from .User import User
from .Like import Like
import datetime


class ReComment(Document):
    writer = StringField(required=True)
    date = DateTimeField(default=datetime.datetime.utcnow)
    like = ReferenceField(Like, default=Like)


class Comment(Document):
    writer = StringField(required=True)
    date = DateTimeField(default=datetime.datetime.utcnow)
    like = ReferenceField(Like, default=Like)
    re_comment = ListField(ReferenceField(ReComment), default=list)
