from flask import Blueprint, jsonify, request
from aimmoPost.aimmoPost.models import User, Post, Like, Comment
from aimmoPost.aimmoPost.config import default
import mongoengine
import sys
import jwt

post = Blueprint("post", __name__, url_prefix="/post")
token_key = default.token


@post.route("/regist", methods=["POST"])
def login():
    try:
        decoded = jwt.decode(request.headers["Token"], token_key, algorithms="HS256")
        data = request.json
        user_id = decoded["user_id"]
        title = data["title"]
        content = data["content"]
        if "tag" in data:
            tag = data["tag"]
        else:
            tag = []
        notice = data["notice"]
        post = Post.Post(writer=user_id, title=title, content=content, tag=tag, notice=notice)
        post.save()
        return jsonify({"success": True})
    except:
        return jsonify({"success": False, "message": str(sys.exc_info()[0])})
    return "post"
