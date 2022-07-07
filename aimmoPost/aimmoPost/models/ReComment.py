from mongoengine import *
from .User import User, UserSchema
import datetime
from marshmallow import fields, Schema, post_load
from .Comment import Comment


class ReComment(Document):
    writer = StringField(required=True)
    date = ComplexDateTimeField(default=datetime.datetime.utcnow)
    content = StringField(required=True)
    like = ListField(ReferenceField(User), default=list)
    comment = ReferenceField(Comment, required=True, reverse_delete_rule=CASCADE)


class ReCommentListSchema(Schema):
    id = fields.Str()
    writer = fields.Str()
    date = fields.DateTime()
    content = fields.Str()
    num_like = fields.Method("like_count")

    def like_count(self, obj):
        return len(obj.like)


class ReCommentDetailSchema(Schema):
    id = fields.Str()
    writer = fields.Str()
    date = fields.DateTime()
    num_like = fields.Method("like_count")
    content = fields.Str()
    like = fields.List(fields.Nested(UserSchema))

    def like_count(self, obj):
        return len(obj.like)


class ReCommentRegistSchema(Schema):
    content = fields.Str()

    @post_load
    def make_recomment(self, data, **kwargs):
        recomment = ReComment(**data)
        return recomment
