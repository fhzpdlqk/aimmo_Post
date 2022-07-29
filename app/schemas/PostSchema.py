from marshmallow import fields, Schema, post_load
from marshmallow.validate import Length
from app.models import Post, Comment, User
from app.schemas.CommentSchema import CommentDetailSchema
from flask import g


class PostListSchema(Schema):
    id = fields.Str(required=True, validate=Length(min=1))
    writer = fields.Method("get_writer")
    date = fields.DateTime()
    title = fields.Str(required=True, validate=Length(min=1))
    content = fields.Str(required=True, validate=Length(min=1))
    tag = fields.List(fields.String)
    notice = fields.Bool(required=True)
    num_like = fields.Int()
    num_comment = fields.Int()
    is_like = fields.Method("islike")

    def get_writer(self, obj) -> str:
        return obj.writer.email

    def islike(self, obj):
        return User.objects(email=g.email).get() in obj.like


class PostRegistSchema(Schema):
    title = fields.Str(required=True)
    content = fields.Str(required=True)
    tag = fields.List(fields.Str(), required=True)
    notice = fields.Bool(default=False)

    @post_load
    def make_post(self, data, **kwargs):
        return dict(data)


class PostDetailSchema(Schema):
    id = fields.Str()
    content = fields.Str()
    title = fields.Str()
    writer = fields.Method("get_writer")
    notice = fields.Bool()
    num_like = fields.Int()
    tag = fields.List(fields.Str())
    date = fields.DateTime()
    num_comment = fields.Int()
    comment = fields.Method("comment_list")

    def get_writer(self, obj) -> str:
        return obj.writer.email

    def comment_list(self, obj):
        return CommentDetailSchema(many=True).dump(Comment.objects(post=obj.id, is_deleted=False))


class PostUpdateSchema(Schema):
    title = fields.Str(required=True)
    content = fields.Str(required=True)
    tag = fields.List(fields.Str(), required=True)
    notice = fields.Bool(default=False)

    @post_load
    def make_post(self, data, **kwargs):
        return dict(data)


class PostSearchSchema(Schema):
    search_word = fields.Str()

    @post_load
    def search_post(self, data, **kwargs):
        return {'search_word': data['search_word']}


class PostListFilterSchema(Schema):
    page = fields.Int()
    size = fields.Int()

    @post_load
    def list_info(self, data, **kwargs):
        return dict(data)
