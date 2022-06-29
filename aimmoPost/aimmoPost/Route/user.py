from flask import Blueprint, jsonify, request
import random
from aimmoPost.aimmoPost.models import User
import mongoengine
import sys


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
    print(random.SystemRandom())
    try:
        data = request.json
        User.User(user_id=data["user_id"], user_pw=data["user_pw"]).save()
        return jsonify({"success": True})
    except mongoengine.errors.NotUniqueError:
        return jsonify({"success": False, "message": "id가 중복되었습니다."})
    except:
        return jsonify({"success": False, "message": str(sys.exc_info()[0])})
