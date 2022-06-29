__version__ = "0.1.0"
import os
from flask import Flask, jsonify


def createApp():
    from .config import default
    import aimmoPost.aimmoPost.Route as Route
    from mongoengine import connect
    from flask_cors import CORS

    connect("connect1", host="mongodb://" + default.mongodb_host + ":" + default.mongodb_port + "/" + default.mongodb_name)

    app = Flask(__name__)
    CORS(app)
    app.register_blueprint(Route.user.user)
    if __name__ == "__main__":
        app.run(debug=True, host="0.0.0.0", port=8000)

    return app
