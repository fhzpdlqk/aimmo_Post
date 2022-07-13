from marshmallow import fields, Schema, post_load
from app.models import ReComment


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
    like = fields.List(fields.Str())

    def like_count(self, obj):
        return len(obj.like)


class ReCommentRegistSchema(Schema):
    content = fields.Str()

    @post_load
    def make_recomment(self, data, **kwargs):
        return {"recomment": ReComment(**data)}
