from flask import Blueprint, jsonify, request
from aimmoPost.aimmoPost.models import User
import mongoengine
import sys
import bcrypt

user = Blueprint("user", __name__, url_prefix="/user")


@user.route("/login", methods=["POST"])
def login():
    try:
        data = request.json
    except:
        pass

    return "login"


"""
    회원가입 API
    method : POST
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


@user.route("/", methods=["POST"])
def signup():
    try:
        data = request.json
        salt = bcrypt.gensalt()
        pw = bcrypt.hashpw(data["user_pw"].encode("utf-8"), salt)
        User.User(user_id=data["user_id"], user_pw=pw, salt=salt).save()
        return jsonify({"success": True})
    except mongoengine.errors.NotUniqueError:
        return jsonify({"success": False, "message": "id가 중복되었습니다."})
    except:
        return jsonify({"success": False, "message": str(sys.exc_info()[0])})
