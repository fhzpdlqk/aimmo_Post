from bson import ObjectId
from flask_classful import FlaskView, route
from flask import g, request
from flask_apispec import marshal_with, use_kwargs, doc
from app.schemas.PostSchema import PostListSchema, PostRegistSchema, PostDetailSchema, PostUpdateSchema, PostSearchSchema, PostListFilterSchema
from app.models import Post, User
from app.decorator import login_required, check_board, check_post, check_post_writer, marshal_empty
from app.errors import ApiError, ApiErrorSchema


class PostView(FlaskView):
    decorators = (doc(tags=["Post"]), check_board, login_required)
    @route("/", methods=["POST"])
    @doc(summary="게시물 작성", description="게시물 작성")
    @use_kwargs(PostRegistSchema())
    @marshal_empty(code=200, description="게시물 작성 성공")
    @marshal_with(ApiErrorSchema, code=422, description="validation error")
    def post(self, board_id, post):
        post.writer = g.user_id
        post.board = ObjectId(board_id)
        post.save()
        return "", 200

    @route("/<string:post_id>", methods=["GET"])
    @doc(summary="게시물 상세 조회", description="게시물 상세 조회")
    @check_post
    @marshal_with(PostDetailSchema, code=200, description="게시물 상세 정보")
    def get_detail(self, board_id, post_id):
        post = Post.objects(board=board_id, id=post_id, is_deleted=False).get()
        return post, 200

    @route("/<string:post_id>", methods=["DELETE"])
    @doc(summary="게시물 삭제", description="게시물 삭제")
    @check_post_writer
    @marshal_empty(code=200, description="게시물 삭제 성공")
    def delete(self, board_id, post_id):
        Post.objects(id=post_id, writer=g.user_id).update(is_deleted=True)
        return "", 200

    @route("/<string:post_id>", methods=["PUT"])
    @doc(summary="게시물 수정", description="게시물 수정")
    @use_kwargs(PostUpdateSchema())
    @check_post_writer
    @marshal_empty(code=200, description="게시물 수정 성공")
    @marshal_with(ApiErrorSchema, code=422, description="validation error")
    def put(self, board_id, post_id, post):
        Post.objects(id=post_id, writer=g.user_id).update(**request.json)
        return "", 200

    @route("/<string:post_id>/like", methods=["POST"])
    @doc(summary="게시물 좋아요", description="게시물 좋아요")
    @check_post
    @marshal_empty(code=200, description="게시물 좋아요 성공")
    @marshal_with(ApiErrorSchema, code=400, description="already like user")
    def like(self, board_id, post_id):
        user = User.objects(user_id=g.user_id).get()
        if user not in Post.objects(id=post_id).get().like:
            Post.objects(id=post_id).update_one(push__like=user)
        else:
            raise ApiError(message="좋아요가 눌러져 있습니다.", status_code=400)
        return "", 200

    @route("/<string:post_id>/like_cancel", methods=["POST"])
    @doc(summary="게시물 좋아요 취소", description="게시물 좋아요 취소")
    @check_post
    @marshal_empty(code=200, description="게시물 좋아요 취소 성공")
    @marshal_with(ApiErrorSchema, code=400, description="no like user")
    def like_cancel(self, board_id, post_id):
        user = User.objects(user_id=g.user_id).get()
        if user in Post.objects(id=post_id).get().like:
            Post.objects(id=post_id).update_one(pull__like=user)
        else:
            raise ApiError(message="좋아요가 눌러져 있지 않습니다.", status_code=400)
        return "", 200

    @route("/search", methods=["POST"])
    @doc(summary="게시물 검색", description="게시물 검색")
    @use_kwargs(PostSearchSchema)
    @marshal_with(PostListSchema(many=True), code=200, description="검색 게시물 리스트")
    def post_search(self, board_id, search_word):
        posts = Post.objects(board=board_id, is_deleted=False, __raw__={"$or": [{"content": {"$regex": request.json["search_word"]}},
                                                              {"title": {"$regex": request.json["search_word"]}}]})
        return posts, 200

    @route("/", methods=["GET"])
    @doc(summary="게시물 목록 조회", description="게시물 목록 조회")
    @use_kwargs(PostListFilterSchema, location='query')
    @marshal_with(PostListSchema(many=True), code=200, description='목록')
    @marshal_with(ApiErrorSchema, code=404, description='적합하지 않은 인덱스')
    def get(self, board_id, size=10, page=1):
        try:
            posts = Post.objects(board=board_id, is_deleted=False).order_by("-notice")[(page - 1) * size: page * size]
            return posts, 200
        except IndexError:
            raise ApiError(message="유효하지 않은 페이지 인덱스 입니다.", status_code=404)
