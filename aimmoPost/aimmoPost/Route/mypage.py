from flask import Blueprint, jsonify, request
import mongoengine
import sys
import jwt
import json
from flask_classful import FlaskView, route
from aimmoPost.aimmoPost.models.Post import Post, PostListSchema
from aimmoPost.aimmoPost.config import default

token_key = default.token


class MyPageView(FlaskView):
    """
    마이페이지 내가 쓴 글 API
    method: GET
    content-type: application/json
    uri: 'mypage/post'
    response : {
        성공시 : {success: true, token: 아이디 토큰}, 200
        토큰이 잘못되었을 경: {success: false, message: 아이디 토큰이 잘못되었습니다.}, 401
        이외의 오류가발생할 경우: {success: False, message: error.message}, 500
    }
    """

    @route("/post", methods=["GET"])
    def my_post(self):
        try:
            decoded = jwt.decode(request.headers["Token"], token_key, algorithms="HS256")
            posts = Post.objects(writer=decoded["user_id"])
            result = []
            for post in posts:
                result.append(PostListSchema().dump(post))
            return jsonify({"success": True, "message": result}), 200

        except jwt.exceptions.InvalidSignatureError:
            return {"success": False, "message": "아이디 토큰이 잘못되었습니다"}, 401
        except:
            return {"success": False, "message": str(sys.exc_info())}, 500
