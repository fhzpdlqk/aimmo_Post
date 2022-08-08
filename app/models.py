from mongoengine import *
import datetime
import jwt
from flask import current_app,g


class User(Document):
    email = EmailField(required=True, unique=True)
    password = StringField(required=True, max_length=100)
    is_master = BooleanField(default=True)


class Board(Document):
    name = StringField(reuired=True)
    is_deleted = BooleanField(default=False)


class Post(Document):
    writer = ReferenceField(User, required=True)
    date = ComplexDateTimeField(default=datetime.datetime.utcnow)
    title = StringField(required=True, max_length=100)
    content = StringField(required=True)
    tag = ListField(StringField(), default=list)
    notice = BooleanField(default=False)
    like = ListField(ReferenceField(User), default=list)
    board = ReferenceField(Board, required=True)
    num_comment = IntField(default=0)
    is_deleted = BooleanField(default=False)

    @property
    def num_like(self) -> int:
        return len(self.like)

    @property
    def comment(self):
        return Comment.objects().filter(post=self)

    @property
    def is_like(self):
        return User.objects().get(email=g.email) in self.like

    @property
    def writer_email(self):
        return self.writer.email


class Comment(Document):
    writer = ReferenceField(User, required=True)
    date = ComplexDateTimeField(default=datetime.datetime.utcnow)
    like = ListField(ReferenceField(User), default=list)
    content = StringField(required=True)
    post = ReferenceField(Post, required=True)
    num_recomment = IntField(default=0)
    is_deleted = BooleanField(default=False)

    @property
    def num_like(self) -> int:
        return len(self.like)

    @property
    def recomment(self):
        return ReComment.objects().filter(comment=self)

    @property
    def writer_email(self):
        return self.writer.email

class ReComment(Document):
    writer = ReferenceField(User, required=True)
    date = ComplexDateTimeField(default=datetime.datetime.utcnow)
    content = StringField(required=True)
    like = ListField(ReferenceField(User), default=list)
    comment = ReferenceField(Comment, required=True)
    is_deleted = BooleanField(default=False)

    @property
    def num_like(self) -> int:
        return len(self.like)

    @property
    def writer_email(self):
        return self.writer.email

class AuthToken(Document):
    token = StringField(required=True)
    @classmethod
    def create(cls, email, is_master):
        token = jwt.encode({"email": email, "is_master": is_master}, current_app.config["TOKEN_KEY"], current_app.config["ALGORITHM"])
        authtoken = cls(token=token)
        return authtoken
