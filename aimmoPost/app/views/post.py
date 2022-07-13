import marshmallow
from bson import ObjectId
from flask_classful import FlaskView, route
from flask import g, jsonify, request
from flask_apispec import marshal_with, use_kwargs
from app.schemas.PostSchema import PostListSchema, PostRegistSchema, PostDetailSchema
from app.models import Post, User
from app.decorator import login_required, check_board, check_post, check_post_writer
from app.schemas.errors import ApiErrorSchema
from app.errors import ApiError


class PostView(FlaskView):

    @route("/", methods=["POST"])
    @login_required
    @check_board
    @use_kwargs(PostRegistSchema(), locations=('json',))
    @marshal_with(ApiErrorSchema, code=422, description="validation error")
    def post(self, board_id, post):
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
        post = Post.objects(board=board_id, id=post_id).get()
        return post, 200

    @route("/<string:post_id>", methods=["DELETE"])
    @login_required
    @check_board
    @check_post_writer
    def delete(self, board_id, post_id):
        Post.objects(id=post_id, writer=g.user_id).delete()
        return "", 200

    @route("/<string:post_id>", methods=["PUT"])
    @login_required
    @check_board
    @check_post_writer
    @marshal_with(ApiErrorSchema, code=422, description="validation error")
    def put(self, board_id, post_id):
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
        posts = Post.objects(board=board_id, __raw__={"$or": [{"content": {"$regex": request.json["search_word"]}},
                                                              {"title": {"$regex": request.json["search_word"]}}]})
        return posts, 200

    @login_required
    @check_board
    @marshal_with(PostListSchema(many=True), code=200, description='검색 목록')
    @marshal_with(ApiErrorSchema, code=404, description='적합하지 않은 인덱스')
    def get(self, board_id):
        try:
            params = request.args.to_dict()
            if "page" not in params:
                params["page"] = "1"
            if "size" not in params:
                params["size"] = "10"
            posts = Post.objects(board=board_id).order_by("-notice")[(int(params["page"]) - 1) * int(params["size"]): int(params["page"]) * int(params["size"])]
            return posts, 200
        except IndexError:
            return ApiError(message="유효하지 않은 페이지 인덱스 입니다."), 404
