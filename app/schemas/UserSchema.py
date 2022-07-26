import bcrypt
from marshmallow import fields, Schema, post_load
from funcy import project
from app.models import User
from app.errors import ApiError


class UserSignupSchema(Schema):
    user_id = fields.Str(required=True)
    user_pw = fields.Str(required=True)
    is_master = fields.Boolean(default=False)

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
        if data["user_origin_pw"] == data["user_pw"]:
            raise ApiError(message="기존 비밀번호와 같습니다", status_code=409)
        return {"user_origin_pw": data["user_origin_pw"], "user_pw": data["user_pw"]}


class AuthTokenSchema(Schema):
    token = fields.Str(required=True)
