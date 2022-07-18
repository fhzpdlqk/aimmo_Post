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
        """ mainpage order by date
            ---
            summary: 최신 게시물 10개
            description: 최신 게시물 10개
            tags: [mainpage]
            security:
                Authorization: []
            responses:
                200:
                    description: Recent 10 posts
                    content:
                        application/json:
                            schema: PostListSchema
                401:
                    description: not login user or not valid token
                    content:
                        application/json:
                            schema: ApiErrorSchema
                422:
                    description: validation error
                    content:
                        application/json:
                            schema: ApiErrorSchema
        """
        post_list = Post.objects(is_deleted=False).order_by("-date")[:10]
        return post_list, 200

    @route("/comment", methods=["GET"])
    @login_required
    @marshal_with(PostListSchema(many=True), code=200, description="게시물 댓글순목록 10개")
    def comment_post(self):
        """ mainpage order by number of comments
            ---
            summary: 댓글 많은 순 게시물 10개
            description: 댓글 많은 순 게시물 10개
            tags: [mainpage]
            security:
                Authorization: []
            responses:
                200:
                    description: Recent 10 posts
                    content:
                        application/json:
                            schema: PostListSchema
                401:
                    description: not login user or not valid token
                    content:
                        application/json:
                            schema: ApiErrorSchema
                422:
                    description: validation error
                    content:
                        application/json:
                            schema: ApiErrorSchema
        """
        post_list = Post.objects(is_deleted=False).order_by("-num_comment")[:10]
        return post_list, 200

    @route("/like", methods=["GET"])
    @login_required
    @marshal_with(PostListSchema(many=True), code=200, description="게시물 좋아요순목록 10개")
    def like_post(self):
        """ mainpage order by like
            ---
            summary: 좋아요 많은 순 게시물 10개
            description: 좋아요 많은 순 게시물 10개
            tags: [mainpage]
            security:
                Authorization: []
            responses:
                200:
                    description: Recent 10 posts
                    content:
                        application/json:
                            schema: PostListSchema
                401:
                    description: not login user or not valid token
                    content:
                        application/json:
                            schema: ApiErrorSchema
                422:
                    description: validation error
                    content:
                        application/json:
                            schema: ApiErrorSchema
        """
        post_list = Post.objects(is_deleted=False).order_by("-like")[:10]
        return post_list, 200
