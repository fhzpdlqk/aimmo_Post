import app.models
import marshmallow.exceptions
import bcrypt
from flask_classful import FlaskView, route
from flask import request, g
from flask_apispec import use_kwargs, marshal_with, doc
from app.schemas.UserSchema import UserSignupSchema, UserSchema, UserLoginSchema, AuthTokenSchema, UserUpdateSchema
from app.models import User, AuthToken
from app.errors import ApiError, ApiErrorSchema
from app.decorator import login_required, marshal_empty


class UserView(FlaskView):
    decorators = (doc(tags=["User"]),)

    @route("/login", methods=["POST"])
    @doc(summary="사용자 로그인", description="사용자 로그인")
    @use_kwargs(UserLoginSchema())
    @marshal_with(AuthTokenSchema, code=200, description='인증 토큰 발급')
    @marshal_with(ApiErrorSchema, code=401, description='로그인 실패')
    def login(self, email, password):
        try:
            user = User.objects().get(email=email)
        except app.models.DoesNotExist:
            raise ApiError(message="존재하지 않는 사용자 입니다.", status_code=401)
        if not bcrypt.checkpw(password.encode("utf-8"), user.password.encode("utf-8")):
            raise ApiError(message="잘못된 비밀번호 입니다.", status_code=401)
        return AuthToken.create(email=email, is_master=user.is_master), 200

    @route("/", methods=["POST"])
    @doc(summary="사용자 회원가입", description="사용자 회원가입")
    @use_kwargs(UserSignupSchema())
    @marshal_empty(code=201, description="회원가입 성공")
    @marshal_with(ApiErrorSchema, code=409, description="이미 존재하는 사용자")
    @marshal_with(ApiErrorSchema, code=422, description="validation 에러")
    def post(self, email, password, is_master=False):
        if User.objects().filter(email=email):
            raise ApiError(message="이미 존재하는 ID입니다.", status_code=409)
        User(email=email, password=password, is_master=is_master).save()
        return "", 201

    @route("/", methods=["PUT"])
    @doc(summary="사용자 비밀번호 변경", description="사용자 비밀번호 변경")
    @login_required
    @use_kwargs(UserUpdateSchema())
    @marshal_empty(code=201, description="비밀번호 변경 성공")
    @marshal_with(ApiErrorSchema, code=401, description="비밀번호가 틀림")
    def put(self, password, origin_password):
        user = User.objects().get(email=g.email)
        if not bcrypt.checkpw(origin_password.encode("utf-8"), user.password.encode("utf-8")):
            raise ApiError(message="비밀번호가 틀립니다.", status_code=401)
        else:
            password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
            User.objects(email=g.email).update(password=password.decode("utf-8"))
            return "", 201
