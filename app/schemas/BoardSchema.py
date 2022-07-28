from marshmallow import fields, Schema, post_load
from app.models import Board


class BoardRegistSchema(Schema):
    name = fields.Str(unique=True, required=True)

    @post_load
    def make_board(self, data, **kwargs):
        return {'board': Board(**data)}


class BoardSchema(Schema):
    name = fields.Str(unique=True, required=True)
    id = fields.Str(required=True)


class BoardUpdateSchema(Schema):
    name = fields.Str(unique=True, required=True)

    @post_load
    def update_board(self, data, **kwargs):
        return {'board': Board(**data)}