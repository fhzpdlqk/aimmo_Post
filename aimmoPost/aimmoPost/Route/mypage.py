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
    @route("/post", methods=["GET"])
    def my_post(self):
        try:
            decoded = jwt.decode(request.headers["Token"], token_key, algorithms="HS256")
            posts = Post.objects()
            result = []
            for post in posts:
                result.append(PostListSchema().dump(post))
            return jsonify({"success": True, "message": result}), 200
        except jwt.exceptions.InvalidSignatureError:
            return {"success": False, "message": "아이디 토큰이 잘못되었습니다"}, 401
        except:
            return {"success": False, "message": str(sys.exc_info())}, 500
