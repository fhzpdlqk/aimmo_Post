from marshmallow import fields, Schema, post_load


class ReCommentListSchema(Schema):
    id = fields.Str()
    writer_email = fields.Email()
    date = fields.DateTime()
    content = fields.Str()
    num_like = fields.Int()



class ReCommentDetailSchema(Schema):
    id = fields.Str()
    writer = fields.Email()
    date = fields.DateTime()
    num_like = fields.Int()
    content = fields.Str()
    like = fields.List(fields.Str())



class ReCommentSchema(Schema):
    content = fields.Str()

