from mongoengine import *
from mongoengine import signals
from .Board import Board
from .User import User, UserSchema
from marshmallow import fields, Schema, post_load, post_dump
import datetime


class Post(Document):
    writer = StringField(required=True)
    date = ComplexDateTimeField(default=datetime.datetime.utcnow)
    title = StringField(required=True, max_length=100)
    content = StringField(required=True)
    tag = ListField(StringField(), default=list)
    notice = BooleanField(default=False)
    like = ListField(ReferenceField(User), default=list)
    board = ReferenceField(Board, required=True)
    num_comment = IntField(default=0)


class PostListSchema(Schema):
    id = fields.Str()
    writer = fields.Str()
    date = fields.DateTime()
    title = fields.Str()
    content = fields.Str()
    tag = fields.List(fields.String)
    notice = fields.Bool()
    num_like = fields.Method("like_count")
    num_comment = fields.Int()

    def like_count(self, obj):
        return len(obj.like)


class PostRegistSchema(Schema):
    title = fields.Str()
    content = fields.Str()
    tag = fields.List(fields.Str())
    notice = fields.Bool()

    @post_load
    def make_post(self, data, **kwargs):
        post = Post(**data)
        return post


class PostDetailSchema(Schema):
    id = fields.Str()
    content = fields.Str()
    title = fields.Str()
    writer = fields.Str()
    notice = fields.Bool()
    num_like = fields.Method("like_count")
    tag = fields.List(fields.Str())
    date = fields.DateTime()
    like = fields.List(fields.Nested(UserSchema))

    def like_count(self, obj):
        return len(obj.like)
