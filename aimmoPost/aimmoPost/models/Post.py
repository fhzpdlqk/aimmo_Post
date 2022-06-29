from mongoengine import *
from .User import User
from .Like import Like
from .Comment import Comment, ReComment
import datetime


class Post(Document):
    writer = ReferenceField(User, required=True)
    date = DateTimeField(default=datetime.datetime.utcnow)
    title = StringField(required=True, max_length=100)
    content = StringField(required=True)
    tag = ListField(StringField(), default=list)
    notice = BooleanField(default=False)
    comment = ReferenceField(Comment)
    like = ReferenceField(Like)
