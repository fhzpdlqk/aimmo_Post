from flask import Blueprint, jsonify, request
from ..models import User

user = Blueprint("user", __name__, url_prefix="/user")


@user.route("/login", methods=["POST", "GET"])
def login():
    return "login"


@user.route("/", methods=["POST"])
def signup():
    content_type = request.headers.get("Content-Type")
    if content_type == "application/json":
        data = request.json
        post = User(_id=data["user_id"], pw=data["user_pw"])
        post.save()
    return jsonify({"success": True})
