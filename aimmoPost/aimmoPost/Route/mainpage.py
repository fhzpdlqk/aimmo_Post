from flask import Blueprint, jsonify, request
import mongoengine
import sys
import jwt
import json
from flask_classful import FlaskView, route
from aimmoPost.aimmoPost.models.Post import Post, PostListSchema


class MainPageView(FlaskView):
    @route("/recent", methods=["GET"])
    def recent_post(self):
        post_list = Post.objects().order_by("-date")[:10]
        result = []
        for post in post_list:
            new_data = PostListSchema().dump(post)
            result.append(new_data)
        return jsonify({"success": True, "message": result}), 200
