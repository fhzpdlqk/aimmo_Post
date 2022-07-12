import marshmallow.exceptions
import bcrypt
import jwt
from flask_classful import FlaskView, route
from flask import jsonify, request, current_app
from app.schemas.UserSchema import UserSignupSchema, UserSchema


class UserView(FlaskView):

    @route("/login", methods=["POST"])
    def login(self):
        try:
            user = UserSchema().load(request.json)
            if not user:
                return {"message": "존재하지 않는 사용자 입니다."}, 401
            if not bcrypt.checkpw(request.json["user_pw"].encode("utf-8"), user.user_pw.encode("utf-8")):
                return {"message": "잘못된 비밀번호 입니다."}, 401
            return {"token": jwt.encode({"user_id": request.json["user_id"], "is_master": user.is_master}, current_app.config["TOKEN_KEY"], current_app.config["ALGORITHM"])}
        except marshmallow.exceptions.ValidationError as err:
            return jsonify({"message": err.messages}), 422

    def post(self):
        try:
            user = UserSignupSchema().load(request.json)
            if user is False:
                return jsonify({"message": "이미 존재하는 ID입니다."}), 409
            user.save()
            return '', 200
        except marshmallow.exceptions.ValidationError as err:
            return jsonify({"message": err.messages}), 422
