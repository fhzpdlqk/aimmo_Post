import marshmallow
from bson import ObjectId
from flask_classful import FlaskView, route
from flask import request, g
from flask_apispec import marshal_with, use_kwargs, doc
from app.models import Comment, User, Post
from app.schemas.Comment import CommentSchema
from app.decorator import login_required, check_post, check_board, check_comment, check_comment_writer, marshal_empty
from app.errors import ApiError, ApiErrorSchema

class CommentView(FlaskView):
    decorators = (doc(tags=["Comment"]),login_required, check_board, check_post)

    @route('/', methods=["POST"])
    @doc(summary="댓글 작성", description="댓글 작성")
    @use_kwargs(CommentSchema())
    @marshal_empty(code=201)
    @marshal_with(ApiErrorSchema, code=422, description="validation error")
    def post(self, board_id, post_id, content):
        post = Post.objects().get(id=post_id)
        Comment(content=content, writer=User.objects().get(email=g.email), post=post).save()
        post.modify(inc__num_comment=1)
        return "", 201

    @route("/<string:comment_id>", methods=["PUT"])
    @doc(summary="댓글 수정", description="댓글 수정")
    @check_comment_writer
    @use_kwargs(CommentSchema())
    @marshal_empty(code=201)
    def put(self, board_id,post_id,comment_id, content):
        Comment.objects().get(id=comment_id, writer=User.objects().get(email=g.email)).update(content=content)
        return "", 201

    @route("/<string:comment_id>", methods=["DELETE"])
    @doc(summary="댓글 삭제", description="댓글 삭제")
    @check_comment_writer
    @marshal_empty(code=204)
    def delete(self, board_id, post_id, comment_id):
        Comment.objects(id=comment_id, writer=User.objects.get(email=g.email)).update(is_deleted=True)
        post = Post.objects().get(id=post_id)
        post.modify(dec__num_comment=1)
        return "", 204


    @route("/<string:comment_id>/like", methods=["POST"])
    @doc(summary="댓글 좋아요", description="댓글 좋아요")
    @check_comment
    @marshal_empty(code=201)
    @marshal_with(ApiErrorSchema, code=400, description="already push like user")
    def like(self, board_id, post_id, comment_id):
        user = User.objects().get(email=g.email)
        if user not in Comment.objects().get(id=comment_id).like:
            Comment.objects(id=comment_id).update_one(push__like=user)
        else:
            raise ApiError(message="이미 좋아요가 눌러져 있습니다", status_code=409)
        return "", 201

    @route("/<string:comment_id>/like", methods=["DELETE"])
    @doc(summary="댓글 좋아요 취소", description="댓글 좋아요 취소")
    @check_comment
    @marshal_empty(code=204)
    @marshal_with(ApiErrorSchema, code=400, description="no push like user")
    def like_cancel(self, board_id, post_id, comment_id):
        user = User.objects().get(email=g.email)
        if user not in Comment.objects().get(id=comment_id).like:
            raise ApiError(message="좋아요가 눌러져 있지 않습니다.", status_code=412)
        else:
            Comment.objects(id=comment_id).update_one(pull__like=user)
        return "", 204
