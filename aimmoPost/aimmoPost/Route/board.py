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
            if "board_name" not in data or data["board_name"] == "":
                return jsonify({"success": False, "message": "게시판 이름을 입력하세요"}), 400
            board = BoardRegistSchema().load(data)
            board.save()
            return jsonify({"success": True}), 200
        except:
            return jsonify({"success": False, "message": str(sys.exc_info()[0])}), 500

    """
        게시판 목록 API
        method: GET
        content-type: application/json
        uri: "/board/list"
        response : {
            성공시 : {success: true, message: [{id,boardname}]}, 200
        }
    """

    @route("/list", methods=["GET"])
    def board_list(self):
        board_name_list = []
        board_list = Board.objects()
        for board in board_list:
            board_name_list.append({"id": str(board.id), "board_name": board.board_name})
        return jsonify({"success": True, "message": board_name_list}), 200

    @route("/<board_id>", methods=["PUT"])
    def board_update(self, board_id):
        try:
            data = request.json
            if "board_name" in data and data["board_name"] == "":
                return jsonify({"success": False, "message": "게시판 이름을 입력해주세요"})
            result = Board.objects(id=board_id).update(**data)

            if result == 1:
                return jsonify({"success": True}), 200
        except mongoengine.errors.ValidationError:
            return jsonify({"success": False, "message": "게시판 아이디가 존재하지 않습니다"}), 404
        except:
            return jsonify({"success": False, "message": str(sys.exc_info()[0])}), 500
