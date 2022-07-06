__version__ = "0.1.0"
import os
from flask import Flask, jsonify

from .config import default
from aimmoPost.aimmoPost.Route import user, post, comment, recomment, board, mainpage
from mongoengine import connect
from flask_cors import CORS


app = Flask(__name__)
app.config["SECRET_KEY"] = "abcd"
app.config["BCRYPT_LEVEL"] = 10

if "DATABASE" not in app.config:
    app.config["DATABASE"] = default.mongodb_uri
try:
    connect("connect1", host=app.config["DATABASE"])
except:
    pass

CORS(app)
user.UserView.register(app, route_base="/user")
post.PostView.register(app, route_base="/post")
comment.CommentView.register(app, route_base="/comment")
recomment.ReCommentView.register(app, route_base="/recomment")
board.BoardView.register(app, route_base="/board")
mainpage.MainPageView.register(app, route_base="/mainpage")
