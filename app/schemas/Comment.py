from marshmallow import fields, Schema, post_load
from app.models import Comment, ReComment
from app.schemas.Recomment import ReCommentDetailSchema, ReCommentListSchema


class CommentListSchema(Schema):
    id = fields.Str()
    writer_email = fields.Email()
    date = fields.DateTime()
    num_like = fields.Int()
    content = fields.Str()



class CommentDetailSchema(Schema):
    id = fields.Str()
    writer_email = fields.Email()
    date = fields.DateTime()
    num_like = fields.Int()
    content = fields.Str()
    like = fields.List(fields.Str())
    recomment = fields.Nested(ReCommentDetailSchema(many=True))
    post = fields.Nested("PostDetailSchema", only=("id",))


class CommentSchema(Schema):
    content = fields.Str()

