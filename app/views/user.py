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
    def login(self, user=False):
        try:
            if not user:
                return ApiError(message="존재하지 않는 사용자 입니다."), 401
            if not bcrypt.checkpw(request.json["user_pw"].encode("utf-8"), user.user_pw.encode("utf-8")):
                return ApiError(message="잘못된 비밀번호 입니다."), 401
            return AuthToken.create(user_id=request.json["user_id"], is_master=user.is_master), 200
        except marshmallow.exceptions.ValidationError as err:
            return ApiError(message=err.messages), 422

    @route("/", methods=["POST"])
    @doc(summary="사용자 회원가입", description="사용자 회원가입")
    @use_kwargs(UserSignupSchema())
    @marshal_with(UserSchema, code=200, description="회원가입 성공")
    @marshal_with(ApiErrorSchema, code=409, description="이미 존재하는 사용자")
    @marshal_with(ApiErrorSchema, code=422, description="validation 에러")
    def post(self, user=None):
        try:
            if User.objects(user_id=user.user_id):
                return ApiError(message="이미 존재하는 ID입니다."), 409
            user.save()
            return user, 200
        except marshmallow.exceptions.ValidationError as err:
            return ApiError(message=err.messages), 422

    @route("/", methods=["PUT"])
    @doc(summary="사용자 비밀번호 변경", description="사용자 비밀번호 변경")
    @login_required
    @use_kwargs(UserUpdateSchema())
    @marshal_empty(code=200, description="비밀번호 변경 성공")
    @marshal_with(ApiErrorSchema, code=401, description="비밀번호가 틀림")
    def put(self, user_pw, user_origin_pw):
        try:
            user = User.objects(user_id=g.user_id).get()
            if not bcrypt.checkpw(user_origin_pw.encode("utf-8"), user.user_pw.encode("utf-8")):
                return ApiError(message="비밀번호가 틀립니다."), 401
            else:
                password = bcrypt.hashpw(user_pw.encode("utf-8"), bcrypt.gensalt())
                User.objects(user_id=g.user_id).update(user_pw = password.decode("utf-8"))
                return "", 200
        except marshmallow.exceptions.ValidationError as err:
            return ApiError(message=err.messages), 422


