from mongoengine import *
import datetime
import jwt
from flask import current_app


class User(Document):
    email = EmailField(required=True, unique=True)
    password = StringField(required=True, max_length=100)
    is_master = BooleanField(default=True)


class Board(Document):
    name = StringField(reuired=True)
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
    def create(cls, email, is_master):
        token = jwt.encode({"email": email, "is_master": is_master}, current_app.config["TOKEN_KEY"], current_app.config["ALGORITHM"])
        authtoken = cls(token=token)
        return authtoken
