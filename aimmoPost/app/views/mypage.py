from flask import jsonify, request, g
import sys
import jwt
from flask_classful import FlaskView, route
from app.schemas.PostSchema import PostListSchema
from app.schemas.CommentSchema import Comment, CommentListSchema
from app.schemas.ReCommentSchema import ReComment, ReCommentListSchema
from app.config import Config
from app.schemas.UserSchema import User
from app.models import Post
from app.decorator import login_required

token_key = Config.TOKEN_KEY


class MyPageView(FlaskView):
    @route("/post", methods=["GET"])
    @login_required
    def my_post(self):
        posts = Post.objects(writer=g.user_id)
        return jsonify(message=PostListSchema(many=True).dump(posts)), 200

    @route("/comment", methods=["GET"])
    @login_required
    def my_comment(self):
        comments = Comment.objects(writer=g.user_id)
        recomments = ReComment.objects(writer=g.user_id)
        return jsonify(comments=CommentListSchema(many=True).dump(comments), recomments=ReCommentListSchema(many=True).dump(recomments)), 200

    @route("/like", methods=["GET"])
    @login_required
    def my_like_post(self):
        #posts = Post.objects.fields(like=[1,{"$elemMatch": {"user_id": g.user_id}}], title=1, writer=1, content=1, date=1, id=1, notice=1, num_comment=1, tag=1, board=1)
        #posts = Post.objects(__raw__={"like": {"$elemMatch": {"user_id": g.user_id}}})
        user = User.objects(user_id=g.user_id).get()
        posts = Post.objects.filter(like__contains=user)
        return jsonify(message=PostListSchema(many=True).dump(posts)), 200
