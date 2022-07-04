from flask import Blueprint, jsonify, request
from aimmoPost.aimmoPost.models import User
from aimmoPost.aimmoPost.config import default
import mongoengine
import sys
import bcrypt
import jwt
from flask_classful import FlaskView, route


class UserView(FlaskView):

    """
    로그인 API
    method: POST
    content-type: application/json
    request : {
        user_id : 윺저 아이디 (String),
        user_pw : 유저 비밀번호 (String)
    }
    response : {
        status : 200, success: true, token: string
        status : 300, success: true, token: string
    }
    """

    @route("/login", methods=["POST"])
    def login(self):
        try:
            data = request.json
            if "user_id" not in data:
                return {"message": "아이디를 입력해주세요"}, 401
            elif "user_pw" not in data:
                return {"message": "비밀번호를 입력해주세요"}, 401
            user_id = data["user_id"]
            user_pw = data["user_pw"]
            for d in User.User.objects(user_id=user_id):
                if bcrypt.checkpw(user_pw.encode("utf-8"), d.user_pw.encode("utf-8")):
                    token = jwt.encode({"user_id": user_id}, default.token, algorithm="HS256")
                    return jsonify({"token": token}), 200
            return {"message": "아이디 혹은 비밀번호가 잘못되었습니다"}, 401
        except:
            return str(sys.exc_info()[0]), 500

    """
        회원가입 API
        method: POST
        content-type: application/json
        request : {
            user_id : 윺저 아이디 (String),
            user_pw : 유저 비밀번호 (String)
        }
        response : {
            status : 200, success: true
            status : 300, success: true
        }
    """

    @route("/", methods=["POST"])
    def signup(self):
        try:
            data = request.json
            salt = bcrypt.gensalt()
            pw = bcrypt.hashpw(data["user_pw"].encode("utf-8"), salt)
            User.User(user_id=data["user_id"], user_pw=pw, salt=salt).save()
            return {"success": True}, 200
        except mongoengine.errors.NotUniqueError:
            return {"success": False, "message": "id가 중복되었습니다."}, 409
        except:
            return {"success": False, "message": str(sys.exc_info()[0])}, 400
