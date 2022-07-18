import marshmallow.exceptions
import bcrypt
from flask_classful import FlaskView, route
from flask import request, g
from flask_apispec import use_kwargs, marshal_with, doc
from app.schemas.UserSchema import UserSignupSchema, UserSchema, UserLoginSchema, AuthTokenSchema, UserUpdateSchema
from app.models import User, AuthToken
from app.errors import ApiError, ApiErrorSchema
from app.decorator import login_required


class UserView(FlaskView):
    decorators=(doc(tags=["User"]),)

    @doc(description="User 로그인", summary="User 로그인")
    @route("/login", methods=["POST"])
    @use_kwargs(UserLoginSchema(), locations=('json',))
    @marshal_with(AuthTokenSchema, code=200, description='인증 토큰 발급')
    @marshal_with(ApiErrorSchema, code=401, description='로그인 실패')
    def login(self, user=False):
        """ user
            --
            summary: 사용자 로그인
            description: 사용자 로그인
            requestBody:
                required: true
                content:
                    application/json:
                        schema: UserLoginSchema
            responses:
                200:
                    description: Return a user token
                    content:
                        application/json:
                            schema: AuthTokenSchema
                401:
                    description: wrong user id or user password
                    content:
                        application/json:
                            schema: ApiErrorSchema
        """
        try:
            if not user:
                return ApiError(message="존재하지 않는 사용자 입니다."), 401
            if not bcrypt.checkpw(request.json["user_pw"].encode("utf-8"), user.user_pw.encode("utf-8")):
                return ApiError(message="잘못된 비밀번호 입니다."), 401
            return AuthToken.create(user_id=request.json["user_id"], is_master=user.is_master), 200
        except marshmallow.exceptions.ValidationError as err:
            return ApiError(message=err.messages), 422

    @use_kwargs(UserSignupSchema(), locations=('json',))
    @marshal_with(UserSchema, code=200, description="회원가입 성공")
    @marshal_with(ApiErrorSchema, code=409, description="이미 존재하는 사용자")
    @marshal_with(ApiErrorSchema, code=422, description="validation 에러")
    def post(self, user=None):
        """ user
            ---
            summary: 사용자 회원가입
            description: 사용자 회원가입
            requestBody:
                required: true
                content:
                    application/json:
                        schema: UserSignupSchema
            responses:
                200:
                    description: Return user information
                    content:
                        application/json:
                            schema: UserSchema
                409:
                    description: duplicate id information
                    content:
                        application/json:
                            schema: ApiErrorSchema
                422:
                    description: validation error
                    content:
                        application/json:
                            schema: ApiErrorSchema
        """
        try:
            if User.objects(user_id=user.user_id):
                return ApiError(message="이미 존재하는 ID입니다."), 409
            user.save()
            return user, 200
        except marshmallow.exceptions.ValidationError as err:
            return ApiError(message=err.messages), 422

    @use_kwargs(UserUpdateSchema(), location=('json',))
    @login_required
    @marshal_with(ApiErrorSchema, code=401, description="비밀번호가 틀림")
    def put(self, user=None):
        """ user
            ---
            summary: 사용자 비밀번호 변경
            description: 사용자 비밀번호 변경
            requestBody:
                required: true
                content:
                    application/json:
                        schema: UserUpdateSchema
            responses:
                200:
                    description: no return
                401:
                    description: not login user or not valid token, or wrong origin password
                    content:
                        application/json:
                            schema: ApiErrorSchema
        """
        if not user:
            return ApiError(message="비밀번호가 틀립니다."), 401
        else:
            User.objects(user_id=g.user_id).get().update(user_pw = bcrypt.hashpw(user.user_pw.encode("utf-8"), bcrypt.gensalt()))
            return "", 200
