from mongoengine import *
from mongoengine import signals
from .User import User, UserSchema
from marshmallow import fields, Schema, post_load, post_dump
import datetime


class Board(Document):
    board_name = StringField(reuired=True)


class BoardRegistSchema(Schema):
    board_name = fields.Str()

    @post_load
    def make_board(self, data, **kwargs):
        board = Board(**data)
        return board
