from mongoengine import *
from .User import User, UserSchema
import datetime
from marshmallow import fields, Schema, post_load
from .Post import Post


class Comment(Document):
    writer = StringField(required=True)
    date = ComplexDateTimeField(default=datetime.datetime.utcnow)
    like = ListField(ReferenceField(User), default=list)
    content = StringField(required=True)
    post = ReferenceField(Post, required=True, reverse_delete_rule=CASCADE)
    num_recomment = IntField(default=0)


class CommentListSchema(Schema):
    id = fields.Str()
    writer = fields.Str()
    date = fields.DateTime()
    num_like = fields.Method("like_count")
    content = fields.Str()

    def like_count(self, obj):
        return len(obj.like)


class CommentDetailSchema(Schema):
    id = fields.Str()
    writer = fields.Str()
    date = fields.DateTime()
    num_like = fields.Method("like_count")
    content = fields.Str()
    like = fields.List(fields.Nested(UserSchema()))

    def like_count(self, obj):
        return len(obj.like)


class CommentRegistSchema(Schema):
    content = fields.Str()

    @post_load
    def make_comment(self, data, **kwargs):
        comment = Comment(**data)
        return comment
