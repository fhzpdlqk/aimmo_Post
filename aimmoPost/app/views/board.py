from flask import jsonify, request, g
from flask_classful import FlaskView, route
import marshmallow.exceptions

from app.models import Board
from app.decorator import login_required, master_required, check_board
from app.schemas.BoardSchema import BoardRegistSchema, BoardSchema, BoardUpdateSchema
from app.schemas.PostSchema import PostListSchema
from app.models import Post, User


class BoardView(FlaskView):

    @login_required
    @master_required
    def post(self):
        try:
            board = BoardRegistSchema().load(request.json)
            if board is False:
                return jsonify(message="이미 등록된 게시판입니다."), 409
            board.save()
            return '', 200
        except marshmallow.exceptions.ValidationError as err:
            return jsonify({"message": err.messages}), 422

    @route("/lists", methods=["GET"])
    def get_list(self):
        board_list = BoardSchema(many=True).dump(Board.objects())
        return jsonify(board_list=board_list), 200

    @route("/<string:board_id>", methods=["PUT"])
    @login_required
    @master_required
    @check_board
    def update(self, board_id):
        try:
            data = BoardUpdateSchema().load(request.json)
            if data is False:
                return jsonify(message="이미 등록된 게시판입니다."), 409
            Board.objects(id=board_id).get().update(**request.json)
            return "", 200
        except marshmallow.exceptions.ValidationError as err:
            return jsonify({"message": err.messages}), 422


    @route("/<string:board_id>", methods=["DELETE"])
    @login_required
    @master_required
    @check_board
    def delete(self, board_id):
        try:
            Board.objects(id=board_id).delete()
            return jsonify({"success": True}), 200
        except marshmallow.exceptions.ValidationError as err:
            return jsonify({"message": err.messages}), 422
