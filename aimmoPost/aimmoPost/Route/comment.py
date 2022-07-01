from flask import Blueprint, jsonify, request
from aimmoPost.aimmoPost.models import User, Post, Like, Comment
from aimmoPost.aimmoPost.config import default
import mongoengine
import sys
import jwt
import json
from flask_classful import FlaskView, route

comment = Blueprint("comment", __name__, url_prefix="/comment")
token_key = default.token


class CommentView(FlaskView):
    @route("/regist", methods=["POST"])
    def comment_regist(self):
        try:
            decoded = jwt.decode(request.headers["Token"], token_key, algorithms="HS256")
            if "id" not in request.args:
                return jsonify({"success": False, "message": "Please input id params"})
            data = request.json
            id = request.args["id"]
            user_id = decoded["user_id"]
            content = data["content"]
            temp = Comment.Comment(writer=user_id, content=content).save()
            result = Post.Post.objects(id=id).update_one(push__comment=temp)
            if result == 1:
                return jsonify({"success": True})
            else:
                return jsonify({"success": False})
        except:
            return jsonify({"success": False, "message": str(sys.exc_info()[0])})
