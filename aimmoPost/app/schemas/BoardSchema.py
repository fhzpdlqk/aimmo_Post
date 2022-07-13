from marshmallow import fields, Schema, post_load
from marshmallow.validate import Length
from app.models import Board


class BoardRegistSchema(Schema):
    board_name = fields.Str(unique=True, required=True, validate=Length(min=1))

    @post_load
    def make_board(self, data, **kwargs):
        board = Board.objects(**data)
        if not board:
            return {'board': Board(**data)}
        return {'board': False}


class BoardSchema(Schema):
    board_name = fields.Str(unique=True, required=True, validate=Length(min=1))
    id = fields.Str(required=True)


class BoardUpdateSchema(Schema):
    board_name = fields.Str(unique=True, required=True, validate=Length(min=1))

    @post_load
    def update_board(self, data, **kwargs):
        if not Board.objects(**data):
            return {'board': True}
        return {'board': False}
