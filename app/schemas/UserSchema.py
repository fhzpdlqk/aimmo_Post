import bcrypt
from marshmallow import fields, Schema, post_load
from app.errors import ApiError


class UserSignupSchema(Schema):
    email = fields.Email(required=True)
    password = fields.Str(required=True)
    is_master = fields.Boolean(default=False)

    @post_load
    def make_user(self, data, **kwargs):
        data["password"] = bcrypt.hashpw(data["password"].encode("utf-8"), bcrypt.gensalt())
        return dict(data)


class UserSchema(Schema):
    email = fields.Email(required=True)
    is_master = fields.Boolean(default=False)


class UserLoginSchema(Schema):
    email = fields.Email()
    password = fields.Str()

    @post_load
    def check_user(self, data, **kwargs):
        return dict(data)


class UserUpdateSchema(Schema):
    origin_password = fields.Str()
    password = fields.Str()

    @post_load
    def check_user(self, data, **kwargs):
        if data["origin_password"] == data["password"]:
            raise ApiError(message="기존 비밀번호와 같습니다", status_code=409)
        return {"origin_password": data["origin_password"], "password": data["password"]}


class AuthTokenSchema(Schema):
    token = fields.Str(required=True)
