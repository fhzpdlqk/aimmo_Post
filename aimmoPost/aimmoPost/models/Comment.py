from mongoengine import *
from .User import User
import datetime
from marshmallow_mongoengine import ModelSchema


class ReComment(Document):
    writer = StringField(required=True)
    date = ComplexDateTimeField(default=datetime.datetime.utcnow)
    content = StringField(required=True)
    like = ListField(ReferenceField(User), default=list)


class Comment(Document):
    writer = StringField(required=True)
    date = ComplexDateTimeField(default=datetime.datetime.utcnow)
    like = ListField(ReferenceField(User), default=list)
    content = StringField(required=True)
    re_comment = ListField(ReferenceField(ReComment), default=list, reverse_delete_rule=CASCADE)


class CommentSchema(ModelSchema):
    class Meta:
        model = Comment


class ReCommentSchema(ModelSchema):
    class Meta:
        model = ReComment
