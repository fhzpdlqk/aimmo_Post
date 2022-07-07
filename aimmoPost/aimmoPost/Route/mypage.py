from flask import Blueprint, jsonify, request
import mongoengine
import sys
import jwt
import json
from flask_classful import FlaskView, route
from aimmoPost.aimmoPost.models.Post import Post
from aimmoPost.aimmoPost.config import default

token_key = default.token


class MyPageView(FlaskView):
    @route("/post", methods=["GET"])
    def my_post(self):
        try:
            decoded = jwt.decode(request.headers["Token"], token_key, algorithms="HS256")
            print(decoded["user_id"])
            post = Post.objects()
            print(post)
        except:
            print(str(sys.exc_info()))
        return "aa"
