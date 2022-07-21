import bcrypt
from flask import g
from marshmallow import fields, Schema, post_load
from funcy import project
from app.models import User


class UserSignupSchema(Schema):
    user_id = fields.Str(required=True)
    user_pw = fields.Str(required=True)

    @post_load
    def make_user(self, data, **kwargs):
        data["user_pw"] = bcrypt.hashpw(data["user_pw"].encode("utf-8"), bcrypt.gensalt())
        user = User(**project(data, ['user_id', 'user_pw', 'is_master']))
        return {'user': user}


class UserSchema(Schema):
    user_id = fields.Str(required=True)
    is_master = fields.Boolean(default=False)


class UserLoginSchema(Schema):
    user_id = fields.Str()
    user_pw = fields.Str()
    is_master = fields.Boolean(default=False)

    @post_load
    def check_user(self, data, **kwargs):
        user = User.objects(user_id=data["user_id"])
        if not user:
            return {'user': False}
        return {'user': user[0]}


class UserUpdateSchema(Schema):
    user_origin_pw = fields.Str()
    user_pw = fields.Str()

    @post_load
    def check_user(self, data, **kwargs):
        return {"user_origin_pw": data["user_origin_pw"], "user_pw": data["user_pw"]}


class AuthTokenSchema(Schema):
    token = fields.Str(required=True)
