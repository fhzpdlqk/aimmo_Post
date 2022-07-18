from mongoengine import *
import datetime
import jwt
from flask import current_app


class User(Document):
    user_id = StringField(required=True, max_length=200, unique=True)
    user_pw = StringField(required=True, max_length=100)
    is_master = BooleanField(default=False)


class Board(Document):
    board_name = StringField(reuired=True)
    is_deleted = BooleanField(default=False)


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
    is_deleted = BooleanField(default=False)

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
    is_deleted = BooleanField(default=False)

class ReComment(Document):
    writer = StringField(required=True)
    date = ComplexDateTimeField(default=datetime.datetime.utcnow)
    content = StringField(required=True)
    like = ListField(ReferenceField(User), default=list)
    comment = ReferenceField(Comment, required=True, reverse_delete_rule=CASCADE)
    is_deleted = BooleanField(default=False)

class AuthToken(Document):
    token = StringField(required=True)
    @classmethod
    def create(cls, user_id, is_master):
        token = jwt.encode({"user_id": user_id, "is_master": is_master}, current_app.config["TOKEN_KEY"], current_app.config["ALGORITHM"])
        authtoken = cls(token=token)
        return authtoken
