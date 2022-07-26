from flask import request
from flask_classful import FlaskView, route
from flask_apispec import use_kwargs, marshal_with, doc
import marshmallow.exceptions

from app.models import Board
from app.decorator import login_required, master_required, check_board, marshal_empty
from app.schemas.BoardSchema import BoardRegistSchema, BoardSchema, BoardUpdateSchema
from app.errors import ApiError, ApiErrorSchema

class BoardView(FlaskView):
    decorators = (doc(tags=["Board"]),)

    @route("/", methods=["POST"])
    @doc(summary="게시판 만들기", description="게시판 만들기")
    @use_kwargs(BoardRegistSchema())
    @login_required
    @master_required
    @marshal_with(ApiErrorSchema, code=409, description="중복 게시판")
    @marshal_with(ApiErrorSchema, code=422, description="validation error")
    @marshal_empty(code=200)
    def post(self, board=False):
        try:
            if not board:
                return ApiError(message="이미 등록된 게시판입니다."), 409
            board.save()
            return '', 200
        except marshmallow.exceptions.ValidationError as err:
            return ApiError(message=err.messages), 422

    @route("/", methods=["GET"])
    @doc(summary="게시판 목록 조회", description="게시판 목록 조회")
    @marshal_with(BoardSchema(many=True), code=200, description="게시판 목록")
    def get(self):
        return Board.objects(), 200

    @route("/<string:board_id>", methods=["PUT"])
    @doc(summary="게시판 이름 수정", description="게시판 이름 수정")
    @use_kwargs(BoardUpdateSchema)
    @login_required
    @master_required
    @check_board
    @marshal_with(ApiErrorSchema, code=409, description='이미 등록된 게시판')
    @marshal_with(ApiErrorSchema, code=422, description='validation error')
    @marshal_empty(code=200)
    def update(self, board_id: str, board=False):
        try:
            if not board:
                return ApiError(message="이미 등록된 게시판입니다."), 409
            Board.objects(id=board_id).get().update(**request.json)
            return "", 200
        except marshmallow.exceptions.ValidationError as err:
            return ApiError({"message": err.messages}), 422

    @route("/<string:board_id>", methods=["DELETE"])
    @doc(summary="게시판 삭제", description="게시판 삭제")
    @login_required
    @master_required
    @check_board
    @marshal_with(ApiErrorSchema, code=422, description='validation error')
    @marshal_empty(code=200)
    def delete(self, board_id):
        try:
            Board.objects(id=board_id).update(is_deleted=True)
            return "", 200
        except marshmallow.exceptions.ValidationError as err:
            return ApiError(message= err.messages), 422
