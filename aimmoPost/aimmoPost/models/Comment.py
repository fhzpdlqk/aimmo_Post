from mongoengine import *
from .User import User
from .Like import Like
import datetime


class ReComment(Document):
    writer = StringField(required=True)
    date = ComplexDateTimeField(default=datetime.datetime.utcnow)
    content = StringField(required=True)
    like = ReferenceField(Like, default=Like)


class Comment(Document):
    writer = StringField(required=True)
    date = ComplexDateTimeField(default=datetime.datetime.utcnow)
    like = ReferenceField(Like, default=Like)
    content = StringField(required=True)
    re_comment = ListField(ReferenceField(ReComment), default=list)
