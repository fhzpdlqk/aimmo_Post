import os
from flask import Flask, jsonify
from mongoengine import connect
from flask_cors import CORS

from app.config import Config
from app.views import register_api
from flask_swagger import swagger

__version__ = "0.1.0"


def create_app(test_config=None):
    app = Flask(__name__)
    app.config.from_object('app.config.Config')
    connect("connect1", host=Config.MONGODB_URI)
    CORS(app)
    register_api(app)

    return app
