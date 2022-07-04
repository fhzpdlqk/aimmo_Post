from mongoengine import *
from .User import User
from .Like import Like
import datetime


class ReComment(Document):
    writer = StringField(required=True)
    date = ComplexDateTimeField(default=datetime.datetime.utcnow)
    content = StringField(required=True)
    like = ListField(ReferenceField(Like), default=list, reverse_delete_rule=CASCADE)


class Comment(Document):
    writer = StringField(required=True)
    date = ComplexDateTimeField(default=datetime.datetime.utcnow)
    like = ListField(ReferenceField(Like), default=list, reverse_delete_rule=CASCADE)
    content = StringField(required=True)
    re_comment = ListField(ReferenceField(ReComment), default=list, reverse_delete_rule=CASCADE)
