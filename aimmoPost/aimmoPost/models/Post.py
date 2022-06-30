from mongoengine import *
from .User import User
from .Like import Like
from .Comment import Comment, ReComment
import datetime


class Post(Document):
    writer = StringField(required=True)
    date = ComplexDateTimeField(default=datetime.datetime.utcnow)
    title = StringField(required=True, max_length=100)
    content = StringField(required=True)
    tag = ListField(StringField(), default=list)
    notice = BooleanField(default=False)
    comment = ListField(ReferenceField(Comment), default=list)
    like = ListField(ReferenceField(Like), default=list)
