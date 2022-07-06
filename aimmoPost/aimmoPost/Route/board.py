from flask import Blueprint, jsonify, request
from aimmoPost.aimmoPost.models.Board import Board, BoardRegistSchema
import mongoengine
import sys
import jwt
import json
from flask_classful import FlaskView, route


class BoardView(FlaskView):
    """
    게시판 생성 API
    method: POST
    content-type: application/json
    uri: "/board/regist"
    request : {
        boardname: 게시판 이름
    }
    response : {
        성공시 : {success: true}, 200
        게시판 이름이 누락되었을 경우 : {success: false,message:"게시판 이름을 입력하세요"}, 400
        이외의 오류가 발생했을 경우 :{success: false, message: error.message},500
    }
    """

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
