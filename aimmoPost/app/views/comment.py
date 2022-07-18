import marshmallow
from bson import ObjectId
from flask_classful import FlaskView, route
from flask import request, g
from flask_apispec import marshal_with, use_kwargs
from app.models import Comment, User, Post
from app.schemas.CommentSchema import CommentRegistSchema
from app.decorator import login_required, check_post, check_board, check_comment, check_comment_writer
from app.errors import ApiError, ApiErrorSchema

class CommentView(FlaskView):
    @route('/', methods=["POST"])
    @login_required
    @check_board
    @check_post
    @use_kwargs(CommentRegistSchema(), locations=('json',))
    @marshal_with(ApiErrorSchema, code=422, description="validation error")
    def post(self, board_id, post_id, comment):
        try:
            comment.writer = g.user_id
            comment.post = ObjectId(post_id)
            comment.save()
            post = Post.objects(id=post_id).get()
            post.update(num_comment=post.num_comment+1)
            return "", 200
        except marshmallow.exceptions.ValidationError as err:
            return ApiError(message=err.messages), 422

    @route("/<string:comment_id>", methods=["PUT"])
    @login_required
    @check_board
    @check_post
    @check_comment_writer
    def put(self, board_id,post_id,comment_id):
        Comment.objects(id=comment_id, writer=g.user_id).update(**request.json)
        return "", 200

    @route("/<string:comment_id>", methods=["DELETE"])
    @login_required
    @check_board
    @check_post
    @check_comment_writer
    def delete(self, board_id, post_id, comment_id):
        Comment.objects(id=comment_id, writer=g.user_id).delete()
        post = Post.objects(id=post_id).get()
        post.update(num_comment=post.num_comment - 1)
        return "", 200


    @route("/<string:comment_id>/like", methods=["POST"])
    @login_required
    @check_board
    @check_post
    @check_comment
    def like(self, board_id, post_id, comment_id):
        user = User.objects(user_id=g.user_id).get()
        if user not in Comment.objects(id=comment_id).get().like:
            Comment.objects(id=comment_id).update_one(push__like=user)
        else:
            Comment.objects(id=comment_id).update_one(pull__like=user)
        return "", 200
