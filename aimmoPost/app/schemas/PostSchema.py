from marshmallow import fields, Schema, post_load
from marshmallow.validate import Length
from app.models import Post, Comment, User
from app.schemas.CommentSchema import CommentDetailSchema
from flask import g


class PostListSchema(Schema):
    id = fields.Str(required=True, validate=Length(min=1))
    writer = fields.Str(required=True, validate=Length(min=1))
    date = fields.DateTime()
    title = fields.Str(required=True, validate=Length(min=1))
    content = fields.Str(required=True, validate=Length(min=1))
    tag = fields.List(fields.String)
    notice = fields.Bool(required=True)
    num_like = fields.Method("like_count")
    num_comment = fields.Int()
    is_like = fields.Method("islike")

    def like_count(self, obj):
        return len(obj.like)

    def islike(self, obj):
        return User.objects(user_id=g.user_id).get() in obj.like


class PostRegistSchema(Schema):
    title = fields.Str(required=True, validate=Length(min=1))
    content = fields.Str(required=True, validate=Length(min=1))
    tag = fields.List(fields.Str())
    notice = fields.Bool(default=False)

    @post_load
    def make_post(self, data, **kwargs):
        return {'post': Post(**data)}


class PostDetailSchema(Schema):
    id = fields.Str()
    content = fields.Str()
    title = fields.Str()
    writer = fields.Str()
    notice = fields.Bool()
    num_like = fields.Method("like_count")
    tag = fields.List(fields.Str())
    date = fields.DateTime()
    num_comment = fields.Int()
    comment = fields.Method("comment_list")

    def like_count(self, obj):
        return len(obj.like)

    def comment_list(self, obj):
        return CommentDetailSchema(many=True).dump(Comment.objects(post=obj.id))


class PostUpdateSchema(Schema):
    title = fields.Str()
    content = fields.Str()
    tag = fields.List(fields.Str())
    notice = fields.Bool(default=False)

    @post_load
    def make_post(self, data, **kwargs):
        return {'post': Post(**data)}
