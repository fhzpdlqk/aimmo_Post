from flask import jsonify, request, g
from flask_classful import FlaskView, route
from flask_apispec import use_kwargs, marshal_with
import marshmallow.exceptions

from app.models import Board
from app.decorator import login_required, master_required, check_board
from app.schemas.BoardSchema import BoardRegistSchema, BoardSchema, BoardUpdateSchema
from app.schemas.errors import ApiErrorSchema
from app.errors import ApiError


class BoardView(FlaskView):

    @use_kwargs(BoardRegistSchema(), locations=('json',))
    @marshal_with(ApiErrorSchema, code=409, description="중복 게시판")
    @marshal_with(ApiErrorSchema, code=422, description="validation error")
    @login_required
    @master_required
    def post(self, board=False):
        try:
            if not board:
                return ApiError(message="이미 등록된 게시판입니다."), 409
            board.save()
            return '', 200
        except marshmallow.exceptions.ValidationError as err:
            return ApiError(message=err.messages), 422

    @marshal_with(BoardSchema(many=True), code=200, description="게시판 목록")
    def get(self):
        return Board.objects(), 200

    @route("/<string:board_id>", methods=["PUT"])
    @use_kwargs(BoardUpdateSchema, locations=('json',))
    @login_required
    @master_required
    @check_board
    @marshal_with(ApiErrorSchema, code=409, description='이미 등록된 게시판')
    @marshal_with(ApiErrorSchema, code=422, description='validation error')
    def update(self, board_id: str, board=False):
        try:
            if not board:
                return ApiError(message="이미 등록된 게시판입니다."), 409
            Board.objects(id=board_id).get().update(**request.json)
            return "", 200
        except marshmallow.exceptions.ValidationError as err:
            return ApiError({"message": err.messages}), 422

    @route("/<string:board_id>", methods=["DELETE"])
    @login_required
    @master_required
    @check_board
    @marshal_with(ApiErrorSchema, code=422, description='validation error')
    def delete(self, board_id):
        try:
            Board.objects(id=board_id).delete()
            return "", 200
        except marshmallow.exceptions.ValidationError as err:
            return ApiError(message= err.messages), 422
