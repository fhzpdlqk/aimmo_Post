from marshmallow import fields, Schema, post_load
from app.models import Comment, ReComment
from app.schemas.ReCommentSchema import ReCommentDetailSchema, ReCommentListSchema


class CommentListSchema(Schema):
    id = fields.Str()
    writer = fields.Method("get_writer")
    date = fields.DateTime()
    num_like = fields.Int()
    content = fields.Str()

    def get_writer(self, obj) -> str:
        return obj.writer.email



class CommentDetailSchema(Schema):
    id = fields.Str()
    writer = fields.Method("get_writer")
    date = fields.DateTime()
    num_like = fields.Int()
    content = fields.Str()
    like = fields.List(fields.Str())
    recomment = fields.Method("recomment_list")

    def get_writer(self, obj) -> str:
        return obj.writer.email

    def recomment_list(self, obj):
        return ReCommentDetailSchema(many=True).dump(ReComment.objects(comment=obj.id, is_deleted=False))


class CommentSchema(Schema):
    content = fields.Str()

    @post_load
    def make_comment(self, data, **kwargs):
        return dict(data)


class CommentMyListSchema(Schema):
    comments = fields.Method("comment_list")
    recomments = fields.Method("recomment_list")

    def comment_list(self, obj) -> object:
        return CommentListSchema(many=True).dump(obj.comment)

    def recomment_list(self, obj) -> object:
        return ReCommentListSchema(many=True).dump(obj.recomment)
