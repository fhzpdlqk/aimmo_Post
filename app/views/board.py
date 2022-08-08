from flask import request
from flask_classful import FlaskView, route
from flask_apispec import use_kwargs, marshal_with, doc

from app.models import Board
from app.decorator import login_required, master_required, check_board, marshal_empty
from app.schemas.Board import BoardRegistSchema, BoardSchema, BoardUpdateSchema
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
    @marshal_empty(code=201)
    def post(self, name):
        if Board.objects().filter(name=name, is_deleted=False):
            raise ApiError(message="이미 등록된 게시판입니다.", status_code=409)
        Board(name=name).save()
        return '', 201

    @route("/", methods=["GET"])
    @doc(summary="게시판 목록 조회", description="게시판 목록 조회")
    @marshal_with(BoardSchema(many=True), code=200, description="게시판 목록")
    def index(self):
        return Board.objects(), 200

    @route("/<string:board_id>", methods=["PUT"])
    @doc(summary="게시판 이름 수정", description="게시판 이름 수정")
    @use_kwargs(BoardUpdateSchema)
    @login_required
    @master_required
    @check_board
    @marshal_with(ApiErrorSchema, code=409, description='이미 등록된 게시판')
    @marshal_with(ApiErrorSchema, code=422, description='validation error')
    @marshal_empty(code=201)
    def update(self, board_id: str, name):
        if Board.objects().filter(name=name, is_deleted=False):
            raise ApiError(message="이미 등록된 게시판입니다.", status_code=409)
        Board.objects().get(id=board_id).update(name=name)
        return "", 201

    @route("/<string:board_id>", methods=["DELETE"])
    @doc(summary="게시판 삭제", description="게시판 삭제")
    @login_required
    @master_required
    @check_board
    @marshal_with(ApiErrorSchema, code=422, description='validation error')
    @marshal_empty(code=204)
    def delete(self, board_id):
        Board.objects(id=board_id).update(is_deleted=True)
        return "", 204
