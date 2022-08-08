from marshmallow import fields, Schema, post_load
from marshmallow.validate import Length
from app.models import Post, Comment, User
from app.schemas.Comment import CommentDetailSchema
from flask import g


class PostListSchema(Schema):
    id = fields.Str(required=True, validate=Length(min=1))
    writer_email = fields.Email()
    date = fields.DateTime()
    title = fields.Str(required=True, validate=Length(min=1))
    content = fields.Str(required=True, validate=Length(min=1))
    tag = fields.List(fields.String)
    notice = fields.Bool(required=True)
    num_like = fields.Int()
    num_comment = fields.Int()
    is_like = fields.Bool()


class PostRegistSchema(Schema):
    title = fields.Str(required=True)
    content = fields.Str(required=True)
    tag = fields.List(fields.Str(), required=True)
    notice = fields.Bool(default=False)



class PostDetailSchema(Schema):
    id = fields.Str()
    content = fields.Str()
    title = fields.Str()
    writer_email = fields.Email()
    notice = fields.Bool()
    num_like = fields.Int()
    tag = fields.List(fields.Str())
    date = fields.DateTime()
    num_comment = fields.Int()
    comment = fields.Nested(CommentDetailSchema(many=True))



class PostUpdateSchema(Schema):
    title = fields.Str(required=True)
    content = fields.Str(required=True)
    tag = fields.List(fields.Str(), required=True)
    notice = fields.Bool(default=False)



class PostSearchSchema(Schema):
    search_word = fields.Str()



class PostListFilterSchema(Schema):
    page = fields.Int()
    size = fields.Int()
