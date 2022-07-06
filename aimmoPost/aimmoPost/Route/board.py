from flask import Blueprint, jsonify, request
from aimmoPost.aimmoPost.models.Board import Board, BoardRegistSchema
import mongoengine
import sys
import jwt
import json
from flask_classful import FlaskView, route


class BoardView(FlaskView):
    @route("/regist", methods=["POST"])
    def board_regist(self):
        try:
            data = request.json
            if "boardname" not in data or data["boardname"] == "":
                return jsonify({"success": False, "message": "게시판 이름을 입력하세요"}), 400
            board = BoardRegistSchema().load(data)
            board.save()
            return jsonify({"success": True}), 200
        except:
            return {"success": False, "message": str(sys.exc_info()[0])}, 500
