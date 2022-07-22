from flask import Flask
from mongoengine import connect
from flask_cors import CORS
from app.config import Config, TestConfig
from app.views import register_api, UserView

__version__ = "0.1.0"


def create_app(test_config=None):
    app = Flask(__name__, static_url_path = '/static')

    app.config.from_object('app.config.Config')
    if test_config != None:
        app.config.from_object('app.config.TestConfig')
        connect("test", host=TestConfig.MONGODB_URI)
    else:
        app.config.from_object('app.config.Config')
        connect("test", host=Config.MONGODB_URI)
    CORS(app)

    register_api(app)

    return app
