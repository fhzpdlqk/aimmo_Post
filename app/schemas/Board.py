from marshmallow import fields, Schema, post_load


class BoardRegistSchema(Schema):
    name = fields.Str(unique=True, required=True)


class BoardSchema(Schema):
    name = fields.Str(unique=True, required=True)
    id = fields.Str(required=True)


class BoardUpdateSchema(Schema):
    name = fields.Str(unique=True, required=True)