__version__ = "0.1.0"
import os
from flask import Flask, jsonify

from .config import default
from aimmoPost.aimmoPost.Route import user, post, comment
from mongoengine import connect
from flask_cors import CORS

connect("connect1", host="mongodb://" + default.mongodb_host + ":" + default.mongodb_port + "/" + default.mongodb_name)

app = Flask(__name__)
app.config["SECRET_KEY"] = "abcd"
app.config["BCRYPT_LEVEL"] = 10

CORS(app)
user.UserView.register(app, route_base="/user")
post.PostView.register(app, route_base="/post")
comment.CommentView.register(app, route_base="/comment")
