from flask import jsonify
from flask_classful import FlaskView, route
from flask_apispec import use_kwargs, marshal_with, doc
from app.schemas.PostSchema import PostListSchema
from app.decorator import login_required
from app.models import Post

class MainPageView(FlaskView):
    decorators = (doc(tags=["Mainpage"]),)
    @route("/recent", methods=["GET"])
    @doc(summary="최근순 게시물 10개", description="최근순 게시물 10개")
    @login_required
    @marshal_with(PostListSchema(many=True), code=200, description="게시물 최근목록 10개")
    def recent_post(self):
        post_list = Post.objects(is_deleted=False).order_by("-date")[:10]
        return post_list, 200

    @route("/comment", methods=["GET"])
    @doc(summary="댓글 많은 순 게시물 10개", description="댓글 많은 순 게시물 10개")
    @login_required
    @marshal_with(PostListSchema(many=True), code=200, description="게시물 댓글순목록 10개")
    def comment_post(self):
        post_list = Post.objects(is_deleted=False).order_by("-num_comment")[:10]
        return post_list, 200

    @route("/like", methods=["GET"])
    @doc(summary="좋아요 많은 순 게시물 10개", description="좋아요 많은 순 게시물 10개")
    @login_required
    @marshal_with(PostListSchema(many=True), code=200, description="게시물 좋아요순목록 10개")
    def like_post(self):
        post_list = Post.objects(is_deleted=False).order_by("-like")[:10]
        return post_list, 200
