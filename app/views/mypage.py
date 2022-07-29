from flask import g
from flask_classful import FlaskView, route
from flask_apispec import marshal_with, doc
from app.schemas.PostSchema import PostListSchema
from app.schemas.CommentSchema import Comment, CommentMyListSchema
from app.schemas.ReCommentSchema import ReComment
from app.schemas.UserSchema import User
from app.models import Post
from app.decorator import login_required

class MyPageView(FlaskView):
    decorators = (doc(tags=["MyPage"]),login_required)
    @route("/posts", methods=["GET"])
    @doc(summary='내가 쓴 게시물', description='내가 쓴 게시물')
    @marshal_with(PostListSchema(many=True), code=200, description="내가 쓴 게시물 목록")
    def my_post(self):
        posts = Post.objects(writer=User.objects().get(email=g.email), is_deleted=False)
        return posts, 200

    @route("/comments", methods=["GET"])
    @doc(summary='내가 쓴 댓글', description='내가 쓴 댓글')
    @marshal_with(CommentMyListSchema, code=200, description="내가 쓴 댓글 목록")
    def my_comment(self):
        comments = Comment.objects(writer=User.objects().get(email=g.email), is_deleted=False)
        recomments = ReComment.objects(writer=User.objects().get(email=g.email), is_deleted=False)
        class ReturnObject():
            def __init__(self, comment, recomment):
                self.comment = comment
                self.recomment = recomment
        return ReturnObject(comments, recomments), 200

    @route("/likes", methods=["GET"])
    @doc(summary='내가 좋아요 한 게시물', description='내가 좋아요 한 게시물')
    @marshal_with(PostListSchema(many=True), code=200, description="내가 좋아요한 게시물 목록")
    def my_like_post(self):
        #posts = Post.objects.fields(like=[1,{"$elemMatch": {"user_id": g.user_id}}], title=1, writer=1, content=1, date=1, id=1, notice=1, num_comment=1, tag=1, board=1)
        #posts = Post.objects(__raw__={"like": {"$elemMatch": {"user_id": g.user_id}}})
        user = User.objects(email=g.email).get()
        posts = Post.objects.filter(like__contains=user, is_deleted=False)
        return posts, 200
