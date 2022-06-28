from flask import Blueprint
from ..models import User

user = Blueprint("user", __name__, url_prefix="/user")


@user.route("/login", methods=["POST", "GET"])
def login():
    post = User(user_id="admin", user_pw="admin")
    post.save()
    return "login"


@user.route("/", methods=["POST"])
def signup():
    return "signup"
