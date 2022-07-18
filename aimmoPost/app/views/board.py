from flask import request
from flask_classful import FlaskView, route
from flask_apispec import use_kwargs, marshal_with, doc
import marshmallow.exceptions

from app.models import Board
from app.decorator import login_required, master_required, check_board
from app.schemas.BoardSchema import BoardRegistSchema, BoardSchema, BoardUpdateSchema
from app.errors import ApiError, ApiErrorSchema

class BoardView(FlaskView):

    @route("/", methods=["POST"])
    @use_kwargs(BoardRegistSchema(), locations=('json',))
    @marshal_with(ApiErrorSchema, code=409, description="중복 게시판")
    @marshal_with(ApiErrorSchema, code=422, description="validation error")
    @login_required
    @master_required
    def post(self, board=False):
        """ board
            ---
            summary: 게시판 만들기 기능
            description: 게시판 만들기 기능
            tags:
                [boards]
            security:
                Authorization: []
            requestBody:
                required: true
                content:
                    application/json:
                        schema: BoardRegistSchema
            responses:
                200:
                    description: no return
                401:
                    description: not login user or not valid token
                    content:
                        application/json:
                            schema: ApiErrorSchema
                403:
                    description: not master user
                    content:
                        application/json:
                            schema: ApiErrorSchema
                409:
                    description: duplicate board name
                    content:
                        application/json:
                            schema: ApiErrorSchema
                422:
                    description: validation error
                    content:
                        application/json:
                            schema: ApiErrorSchema
        """
        try:
            if not board:
                return ApiError(message="이미 등록된 게시판입니다."), 409
            board.save()
            return '', 200
        except marshmallow.exceptions.ValidationError as err:
            return ApiError(message=err.messages), 422

    @route("/", methods=["GET"])
    @marshal_with(BoardSchema(many=True), code=200, description="게시판 목록")
    def get(self):
        """ board
            ---
            summary: 게시판 목록 조회
            description: 게시판 목록 조회
            tags:
                [boards]
            responses:
                200:
                    description: return board list
                    content:
                        application/json:
                            schema: BoardSchema
        """
        return Board.objects(), 200

    @route("/<string:board_id>", methods=["PUT"])
    @use_kwargs(BoardUpdateSchema, locations=('json',))
    @login_required
    @master_required
    @check_board
    @marshal_with(ApiErrorSchema, code=409, description='이미 등록된 게시판')
    @marshal_with(ApiErrorSchema, code=422, description='validation error')
    def update(self, board_id: str, board=False):
        """ board
            ---
            summary: 게시판 이름 수정
            description: 게시판 이름 수정
            tags:
                [boards]
            parameters:
                board_id: []
            security:
                Authorization: []
            requestBody:
                required: true
                content:
                    application/json:
                        schema: BoardUpdateSchema
            responses:
                200:
                    description: no return
                401:
                    description: not login user or not valid token
                    content:
                        application/json:
                            schema: ApiErrorSchema
                403:
                    description: not master user
                    content:
                        application/json:
                            schema: ApiErrorSchema
                404:
                    description: not found board id
                    content:
                        application/json:
                            schema: ApiErrorSchema
                409:
                    description: duplicate board name
                    content:
                        application/json:
                            schema: ApiErrorSchema
                422:
                    description: validation error
                    content:
                        application/json:
                            schema: ApiErrorSchema
        """
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
        """ board
            ---
            summary: 게시판 삭제
            description: 게시판 삭제
            tags:
                [boards]
            parameters:
                board_id: []
            security:
                Authorization: []
            responses:
                200:
                    description: no return
                401:
                    description: not login user or not valid token
                    content:
                        application/json:
                            schema: ApiErrorSchema
                403:
                    description: not master user
                    content:
                        application/json:
                            schema: ApiErrorSchema
                404:
                    description: not found board id
                    content:
                        application/json:
                            schema: ApiErrorSchema
                409:
                    description: duplicate board name
                    content:
                        application/json:
                            schema: ApiErrorSchema
                422:
                    description: validation error
                    content:
                        application/json:
                            schema: ApiErrorSchema
        """
        try:
            Board.objects(id=board_id).delete()
            return "", 200
        except marshmallow.exceptions.ValidationError as err:
            return ApiError(message= err.messages), 422
