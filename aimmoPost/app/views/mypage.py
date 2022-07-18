from flask import jsonify, g
from flask_classful import FlaskView, route
from flask_apispec import marshal_with, use_kwargs
from app.schemas.PostSchema import PostListSchema
from app.schemas.CommentSchema import Comment, CommentListSchema, CommentMyListSchema
from app.schemas.ReCommentSchema import ReComment, ReCommentListSchema
from app.schemas.UserSchema import User
from app.models import Post
from app.decorator import login_required

class MyPageView(FlaskView):
    @route("/posts", methods=["GET"])
    @login_required
    @marshal_with(PostListSchema(many=True), code=200, description="내가 쓴 게시물 목록")
    def my_post(self):
        """ my post
            ---
            summary: 내가 쓴 게시물 목록
            description: 내가 쓴 게시물 목록
            tags: [mypage]
            security:
                Authorization: [Authorization]
            responses:
                200:
                    description: return lists written by me
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
        posts = Post.objects(writer=g.user_id, is_deleted=False)
        return posts, 200

    @route("/comments", methods=["GET"])
    @login_required
    @marshal_with(CommentMyListSchema, code=200, description="내가 쓴 댓글 목록")
    def my_comment(self):
        """ my comment
            ---
            summary: 내가 쓴 댓글 목록
            description: 내가 쓴 댓글 목록
            tags: [mypage]
            security:
                Authorization: [Authorization]
            responses:
                200:
                    description: return comments and recomments written by me
                    content:
                        application/json:
                            schema: CommentMyListSchema
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
        comments = Comment.objects(writer=g.user_id, is_deleted=False)
        recomments = ReComment.objects(writer=g.user_id, is_deleted=False)
        class ReturnObject():
            def __init__(self, comment, recomment):
                self.comment = comment
                self.recomment = recomment
        return ReturnObject(comments, recomments), 200

    @route("/likes", methods=["GET"])
    @login_required
    @marshal_with(PostListSchema(many=True), code=200, description="내가 좋아요한 게시물 목록")
    def my_like_post(self):
        """ my like post
            ---
            summary: 내가 좋아요 한 게시물 목록
            description: 내가 좋아요 한 게시물 목록
            tags: [mypage]
            security:
                Authorization: [Authorization]
            responses:
                200:
                    description: return posts liked by me
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
        #posts = Post.objects.fields(like=[1,{"$elemMatch": {"user_id": g.user_id}}], title=1, writer=1, content=1, date=1, id=1, notice=1, num_comment=1, tag=1, board=1)
        #posts = Post.objects(__raw__={"like": {"$elemMatch": {"user_id": g.user_id}}})
        user = User.objects(user_id=g.user_id).get()
        posts = Post.objects.filter(like__contains=user, is_deleted=False)
        return posts, 200
