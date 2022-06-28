import os
from flask import Flask, jsonify
from flask_cors import CORS
import Route

app = Flask(__name__)
CORS(app)

app.register_blueprint(Route.user.user)
if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8000)
