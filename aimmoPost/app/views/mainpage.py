from flask import jsonify
from flask_classful import FlaskView, route
from flask_apispec import use_kwargs, marshal_with
from app.schemas.PostSchema import PostListSchema
from app.decorator import login_required
from app.models import Post

class MainPageView(FlaskView):
    @route("/recent", methods=["GET"])
    @login_required
    @marshal_with(PostListSchema(many=True), code=200, description="게시물 최근목록 10개")
    def recent_post(self):
        post_list = Post.objects().order_by("-date")[:10]
        return post_list, 200

    @route("/comment", methods=["GET"])
    @login_required
    @marshal_with(PostListSchema(many=True), code=200, description="게시물 댓글순목록 10개")
    def comment_post(self):
        post_list = Post.objects().order_by("-num_comment")[:10]
        return post_list, 200

    @route("/like", methods=["GET"])
    @login_required
    @marshal_with(PostListSchema(many=True), code=200, description="게시물 좋아요순목록 10개")
    def like_post(self):
        post_list = Post.objects().order_by("-like")[:10]
        return post_list, 200
