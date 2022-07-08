import bcrypt
from marshmallow import fields, Schema, post_load
from app.models import User


class UserSignupSchema(Schema):
    user_id = fields.Str(required=True, unique=True)
    user_pw = fields.Str(required=True)
    is_master = fields.Boolean(default=False)

    @post_load
    def make_user(self, data, **kwargs):
        if not User.objects(user_id=data["user_id"]):
            data["user_pw"] = bcrypt.hashpw(data["user_pw"].encode("utf-8"), bcrypt.gensalt())
            return User(**data)
        return False

class UserSchema(Schema):
    user_id = fields.Str(required=True, unique=True)
    user_pw = fields.Str(required=True)

    @post_load
    def check_user(self, data, **kwargs):
        if not User.objects(user_id=data["user_id"]):
            return False
        return User.objects(user_id=data["user_id"]).get()
