from mongoengine import *
from marshmallow_mongoengine import ModelSchema


class User(Document):
    user_id = StringField(required="True", max_length=200, unique=True)
    user_pw = StringField(required="True", max_length=100)
    salt = StringField(required="True", max_length=100)


class UserSchema(ModelSchema):
    class Meta:
        model = User
