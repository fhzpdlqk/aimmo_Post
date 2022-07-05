from mongoengine import *
from mongoengine import signals
from .User import User
from .Comment import Comment, ReComment
from .Like import Like
import datetime


class Post(Document):
    writer = StringField(required=True)
    date = ComplexDateTimeField(default=datetime.datetime.utcnow)
    title = StringField(required=True, max_length=100)
    content = StringField(required=True)
    tag = ListField(StringField(), default=list)
    notice = BooleanField(default=False)
    comment = ListField(ReferenceField(Comment, reverse_delete_rule=CASCADE), default=list)
    like = ListField(ReferenceField(User), default=list)
