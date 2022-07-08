from marshmallow import fields, Schema, post_load
from app.models import Comment, ReComment
from app.schemas.ReCommentSchema import ReCommentDetailSchema


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
    like = fields.List(fields.Str())
    recomment = fields.Method("recomment_list")

    def like_count(self, obj):
        return len(obj.like)
    def recomment_list(self,obj):
        return ReCommentDetailSchema(many=True).dump(ReComment.objects(comment=obj.id))


class CommentRegistSchema(Schema):
    content = fields.Str()

    @post_load
    def make_comment(self, data, **kwargs):
        comment = Comment(**data)
        return comment
