import os
from flask import Flask, jsonify

# from flask_cors import CORS
from . import config
from . import Route
from mongoengine import *

connect("connect1", host="mongodb://" + config.default.mongodb_host + ":" + config.default.mongodb_port + "/" + config.default.mongodb_name)


app = Flask(__name__)
# CORS(app)

app.register_blueprint(Route.user.user)
if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8000)
