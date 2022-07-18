import marshmallow
from bson import ObjectId
from flask_classful import FlaskView, route
from flask import g, request
from flask_apispec import marshal_with, use_kwargs
from app.schemas.PostSchema import PostListSchema, PostRegistSchema, PostDetailSchema, PostUpdateSchema
from app.models import Post, User
from app.decorator import login_required, check_board, check_post, check_post_writer
from app.errors import ApiError, ApiErrorSchema


class PostView(FlaskView):

    @route("/", methods=["POST"])
    @login_required
    @check_board
    @use_kwargs(PostRegistSchema(), locations=('json',))
    @marshal_with(ApiErrorSchema, code=422, description="validation error")
    def post(self, board_id, post):
        """ write post
            ---
            summary: 게시물 글쓰기 기능
            description: 게시물 글쓰기 기능
            tags: [posts]
            security:
                Authorization: []
            parameters:
                board_id: []
            requestBody:
                required: true
                content:
                    application/json:
                        schema: PostRegistSchema
            responses:
                200:
                    description: no return
                401:
                    description: not login user or not valid token
                    content:
                        application/json:
                            schema: ApiErrorSchema
                404:
                    description: not found board id
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
            post.writer = g.user_id
            post.board = ObjectId(board_id)
            post.save()
            return "", 200
        except marshmallow.exceptions.ValidationError as err:
            return ApiError(message=err.messages), 422

    @route("/<string:post_id>", methods=["GET"])
    @login_required
    @check_board
    @check_post
    @marshal_with(PostDetailSchema, code=200, description="게시물 상세 정보")
    def get_detail(self, board_id, post_id):
        """ get_detail_posts
            ---
            summary: 게시물 상세조회
            description: 게시물 상세조회
            tags: [posts]
            security:
                Authorization: []
            parameters:
                board_id: []
                post_id: []
            responses:
                200:
                    description: post detail inforamtion
                    content:
                        application/json:
                            schema: PostDetailSchema
                401:
                    description: not login user or not valid token
                    content:
                        application/json:
                            schema: ApiErrorSchema
                404:
                    description: not found board id or post id
                    content:
                        application/json:
                            schema: ApiErrorSchema
                422:
                    description: validation error
                    content:
                        application/json:
                            schema: ApiErrorSchema
        """
        post = Post.objects(board=board_id, id=post_id, is_deleted=False).get()
        return post, 200

    @route("/<string:post_id>", methods=["DELETE"])
    @login_required
    @check_board
    @check_post_writer
    def delete(self, board_id, post_id):
        """ delete post
            ---
            summary: 게시물 삭제
            description: 게시물 삭제
            tags: [posts]
            security:
                Authorization: []
            parameters:
                board_id: []
                post_id: []
            responses:
                200:
                    description: no returns
                401:
                    description: not login user or not valid token
                    content:
                        application/json:
                            schema: ApiErrorSchema
                404:
                    description: not found board id or post id
                    content:
                        application/json:
                            schema: ApiErrorSchema
        """
        Post.objects(id=post_id, writer=g.user_id).update(is_deleted=True)
        return "", 200

    @route("/<string:post_id>", methods=["PUT"])
    @use_kwargs(PostUpdateSchema(), locations=('json',))
    @login_required
    @check_board
    @check_post_writer
    @marshal_with(ApiErrorSchema, code=422, description="validation error")
    def put(self, board_id, post_id, post):
        """ update post
            ---
            summary: 게시물 수정
            description: 게시물 수정
            tags: [posts]
            security:
                Authorization: []
            parameters:
                board_id: []
                post_id: []
            requestBody:
                required: true
                content:
                    application/json:
                        schema: PostUpdateSchema
            responses:
                200:
                    description: no returns
                401:
                    description: not login user or not valid token
                    content:
                        application/json:
                            schema: ApiErrorSchema
                404:
                    description: not found board id or post id
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
            Post.objects(id=post_id, writer=g.user_id).update(**request.json)
            return "", 200
        except marshmallow.exceptions.ValidationError as err:
            return ApiError(message=err.messages), 422

    @route("/<string:post_id>/like", methods=["POST"])
    @login_required
    @check_board
    @check_post
    def like(self, board_id, post_id):
        """ like post
            ---
            summary: 게시물 좋아요
            description: 게시물 좋아요
            tags: [posts]
            security:
                Authorization: []
            parameters:
                board_id: []
                post_id: []
            responses:
                200:
                    description: no returns
                401:
                    description: not login user or not valid token
                    content:
                        application/json:
                            schema: ApiErrorSchema
                404:
                    description: not found board id or post id
                    content:
                        application/json:
                            schema: ApiErrorSchema
        """
        user = User.objects(user_id=g.user_id).get()
        if user not in Post.objects(id=post_id).get().like:
            Post.objects(id=post_id).update_one(push__like=user)
        else:
            Post.objects(id=post_id).update_one(pull__like=user)
        return "", 200

    @route("/search", methods=["POST"])
    @login_required
    @check_board
    @marshal_with(PostListSchema(many=True), code=200, description="검색 게시물 리스트")
    def post_search(self, board_id):
        """ search post
            ---
            summary: 게시물 검색
            description: 게시물 검색
            tags: [posts]
            security:
                Authorization: []
            requestBody:
                required: true
                content:
                    application/json:
                        schema:
                            type: object
                            properties:
                                search_word:
                                    type: string
            responses:
                200:
                    description: search post list
                    content:
                        application/json:
                            schema: PostListSchema
                401:
                    description: not login user or not valid token
                    content:
                        application/json:
                            schema: ApiErrorSchema
                404:
                    description: not found board id
                    content:
                        application/json:
                            schema: ApiErrorSchema
        """
        posts = Post.objects(board=board_id, is_deleted=False, __raw__={"$or": [{"content": {"$regex": request.json["search_word"]}},
                                                              {"title": {"$regex": request.json["search_word"]}}]})
        return posts, 200

    @route("/", methods=["GET"])
    @login_required
    @check_board
    @marshal_with(PostListSchema(many=True), code=200, description='목록')
    @marshal_with(ApiErrorSchema, code=404, description='적합하지 않은 인덱스')
    def get(self, board_id):
        """ post list
            ---
            summary: 게시물 목록 조회
            description: 게시물 목록 조회
            tags: [posts]
            security:
                Authorization: []
            parameters:
                board_id: []
                page: []
                size: []
            responses:
                200:
                    description: post list return
                    content:
                        application/json:
                            schema: PostListSchema
                401:
                    description: not login user or not valid token
                    content:
                        application/json:
                            schema: ApiErrorSchema
                404:
                    description: not found board id
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
            params = request.args.to_dict()
            if "page" not in params:
                params["page"] = "1"
            if "size" not in params:
                params["size"] = "10"
            posts = Post.objects(board=board_id, is_deleted=False).order_by("-notice")[(int(params["page"]) - 1) * int(params["size"]): int(params["page"]) * int(params["size"])]
            return posts, 200
        except IndexError:
            return ApiError(message="유효하지 않은 페이지 인덱스 입니다."), 404
