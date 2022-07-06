from mongoengine import *
from .User import User, UserSchema
import datetime
from marshmallow import fields, Schema, post_load


class ReComment(Document):
    writer = StringField(required=True)
    date = ComplexDateTimeField(default=datetime.datetime.utcnow)
    content = StringField(required=True)
    like = ListField(ReferenceField(User), default=list)


class Comment(Document):
    writer = StringField(required=True)
    date = ComplexDateTimeField(default=datetime.datetime.utcnow)
    like = ListField(ReferenceField(User), default=list)
    content = StringField(required=True)
    re_comment = ListField(ReferenceField(ReComment), default=list, reverse_delete_rule=CASCADE)


class ReCommentDetailSchema(Schema):
    id = fields.Str()
    writer = fields.Str()
    date = fields.DateTime()
    num_like = fields.Method("like_count")
    content = fields.Str()
    like = fields.List(fields.Nested(UserSchema))

    def like_count(self, obj):
        return len(obj.like)


class CommentDetailSchema(Schema):
    id = fields.Str()
    writer = fields.Str()
    date = fields.DateTime()
    num_like = fields.Method("like_count")
    content = fields.Str()
    recomment = fields.List(fields.Nested(ReCommentDetailSchema()))
    like = fields.List(fields.Nested(UserSchema()))

    def like_count(self, obj):
        return len(obj.like)


class CommentRegistSchema(Schema):
    content = fields.Str()

    @post_load
    def make_comment(self, data, **kwargs):
        comment = Comment(**data)
        return comment


class ReCommentRegistSchema(Schema):
    content = fields.Str()

    @post_load
    def make_recomment(self, data, **kwargs):
        recomment = ReComment(**data)
        return recomment
