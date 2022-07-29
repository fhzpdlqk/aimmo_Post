from marshmallow import fields, Schema, post_load


class BoardRegistSchema(Schema):
    name = fields.Str(unique=True, required=True)

    @post_load
    def make_board(self, data, **kwargs):
        return {'board_name': data["name"]}


class BoardSchema(Schema):
    name = fields.Str(unique=True, required=True)
    id = fields.Str(required=True)


class BoardUpdateSchema(Schema):
    name = fields.Str(unique=True, required=True)

    @post_load
    def update_board(self, data, **kwargs):
        return dict(data)