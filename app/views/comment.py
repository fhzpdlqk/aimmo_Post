import marshmallow
from bson import ObjectId
from flask_classful import FlaskView, route
from flask import request, g
from flask_apispec import marshal_with, use_kwargs, doc
from app.models import Comment, User, Post
from app.schemas.CommentSchema import CommentSchema
from app.decorator import login_required, check_post, check_board, check_comment, check_comment_writer, marshal_empty
from app.errors import ApiError, ApiErrorSchema

class CommentView(FlaskView):
    decorators = (doc(tags=["Comment"]),)

    @route('/', methods=["POST"])
    @doc(summary="댓글 작성", description="댓글 작성")
    @login_required
    @check_board
    @check_post
    @use_kwargs(CommentSchema())
    @marshal_empty(code=200)
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
    @doc(summary="댓글 수정", description="댓글 수정")
    @login_required
    @check_board
    @check_post
    @check_comment_writer
    @marshal_empty(code=200)
    @use_kwargs(CommentSchema())
    def put(self, board_id,post_id,comment_id, comment):
        Comment.objects(id=comment_id, writer=g.user_id).update(**request.json)
        return "", 200

    @route("/<string:comment_id>", methods=["DELETE"])
    @doc(summary="댓글 삭제", description="댓글 삭제")
    @login_required
    @check_board
    @check_post
    @check_comment_writer
    @marshal_empty(code=200)
    def delete(self, board_id, post_id, comment_id):
        Comment.objects(id=comment_id, writer=g.user_id).update(is_deleted=True)
        post = Post.objects(id=post_id).get()
        post.update(num_comment=post.num_comment - 1)
        return "", 200


    @route("/<string:comment_id>/like", methods=["POST"])
    @doc(summary="댓글 좋아요", description="댓글 좋아요")
    @login_required
    @check_board
    @check_post
    @check_comment
    @marshal_empty(code=200)
    @marshal_with(ApiErrorSchema, code=400, description="already push like user")
    def like(self, board_id, post_id, comment_id):
        user = User.objects(user_id=g.user_id).get()
        if user not in Comment.objects(id=comment_id).get().like:
            Comment.objects(id=comment_id).update_one(push__like=user)
        else:
            return ApiError(message="이미 좋아요가 눌러져 있습니다"), 400
        return "", 200

    @route("/<string:comment_id>/like_cancel", methods=["POST"])
    @doc(summary="댓글 좋아요 취소", description="댓글 좋아요 취소")
    @login_required
    @check_board
    @check_post
    @check_comment
    @marshal_empty(code=200)
    @marshal_with(ApiErrorSchema, code=400, description="no push like user")
    def like_cancel(self, board_id, post_id, comment_id):
        user = User.objects(user_id=g.user_id).get()
        if user not in Comment.objects(id=comment_id).get().like:
            return ApiError(message="좋아요가 눌러져 있지 않습니다."), 400
        else:
            Comment.objects(id=comment_id).update_one(pull__like=user)
        return "", 200
