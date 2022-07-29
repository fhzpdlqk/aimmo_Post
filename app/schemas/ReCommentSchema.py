from marshmallow import fields, Schema, post_load


class ReCommentListSchema(Schema):
    id = fields.Str()
    writer = fields.Method("get_writer")
    date = fields.DateTime()
    content = fields.Str()
    num_like = fields.Int()

    def get_writer(self, obj) -> str:
        return obj.writer.email


class ReCommentDetailSchema(Schema):
    id = fields.Str()
    writer = fields.Method("get_writer")
    date = fields.DateTime()
    num_like = fields.Int()
    content = fields.Str()
    like = fields.List(fields.Str())

    def get_writer(self, obj) -> str:
        return obj.writer.email


class ReCommentSchema(Schema):
    content = fields.Str()

    @post_load
    def make_recomment(self, data, **kwargs):
        return dict(data)
