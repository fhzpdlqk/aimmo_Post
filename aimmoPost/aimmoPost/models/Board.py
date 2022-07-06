from mongoengine import *
from mongoengine import signals
from .User import User, UserSchema
from .Comment import Comment, ReComment, CommentDetailSchema, ReCommentDetailSchema
from marshmallow import fields, Schema, post_load, post_dump
import datetime
from .Post import Post


class Board(Document):
    boardname = StringField(reuired=True)
    post = ListField(ReferenceField(Post, reverse_delete_rule=CASCADE), default=list)


class BoardRegistSchema(Schema):
    boardname = fields.Str()

    @post_load
    def make_board(self, data, **kwargs):
        board = Board(**data)
        return board
