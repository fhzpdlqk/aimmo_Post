import mongoengine
from mongoengine import *
from mongoengine import signals
import datetime


class User(Document):
    user_id = StringField(required=True, max_length=200, unique=True)
    user_pw = StringField(required=True, max_length=100)
    is_master = BooleanField(default=False)


class Board(Document):
    board_name = StringField(reuired=True, unique=True)


class Post(Document):
    writer = StringField(required=True)
    date = ComplexDateTimeField(default=datetime.datetime.utcnow)
    title = StringField(required=True, max_length=100)
    content = StringField(required=True)
    tag = ListField(StringField(), default=list)
    notice = BooleanField(default=False)
    like = ListField(ReferenceField(User), default=list)
    board = ReferenceField(Board)
    num_comment = IntField(default=0)

    @classmethod
    def post_save(cls, sender, document, **kwargs):
        post = Post.objects(id=document.post).get()
        post.update(num_comment=post.num_comment + 1)

    @classmethod
    def post_delete(cls, sender, document, **kwargs):
        post = Post.objects(id=document.post).get()
        post.update(num_comment=post.num_comment - 1)


class Comment(Document):
    writer = StringField(required=True)
    date = ComplexDateTimeField(default=datetime.datetime.utcnow)
    like = ListField(ReferenceField(User), default=list)
    content = StringField(required=True)
    post = ReferenceField(Post)
    num_recomment = IntField(default=0)

class ReComment(Document):
    writer = StringField(required=True)
    date = ComplexDateTimeField(default=datetime.datetime.utcnow)
    content = StringField(required=True)
    like = ListField(ReferenceField(User), default=list)
    comment = ReferenceField(Comment, required=True, reverse_delete_rule=CASCADE)
