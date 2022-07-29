from flask import request, g
from bson import ObjectId
from flask_classful import FlaskView, route
from flask_apispec import use_kwargs, marshal_with, doc
from app.models import ReComment, User, Comment
from app.schemas.ReCommentSchema import ReCommentSchema
from app.decorator import login_required, check_board, check_post, check_comment, check_recomment_writer, check_recomment, marshal_empty
from app.errors import ApiError, ApiErrorSchema

class ReCommentView(FlaskView):
    decorators = (doc(tags=["ReComment"]), login_required, check_board, check_post, check_comment)

    @route("/",methods=["POST"])
    @doc(summary="대댓글 작성", description="대댓글 작성")
    @use_kwargs(ReCommentSchema)
    @marshal_empty(code=200, description="대댓글 작성 성공")
    @marshal_with(ApiErrorSchema, code=422, description='validation error')
    def post(self, board_id, post_id, comment_id, recomment):
        recomment.writer = User.objects().get(email=g.email)
        recomment.comment = ObjectId(comment_id)
        recomment.save()
        comment = Comment.objects(id=comment_id).get()
        comment.update(num_recomment=comment.num_recomment + 1)
        return "", 200

    @route("/<recomment_id>", methods=["PUT"])
    @doc(summary="대댓글 수정", description="대댓글 수정")
    @check_recomment_writer
    @marshal_empty(code=200, description="대댓글 수정 성공")
    @use_kwargs(ReCommentSchema)
    def put(self, board_id, post_id, comment_id, recomment_id, recomment):
        ReComment.objects(id=recomment_id, writer=User.objects.get(email=g.email)).update(**request.json)
        return "", 200

    @route("/<recomment_id>", methods=["DELETE"])
    @doc(summary="대댓글 삭제", description="대댓글 삭제")
    @check_recomment_writer
    @marshal_empty(code=200, description="대댓글 삭제 성공")
    def delete(self, board_id, post_id, comment_id, recomment_id):
        ReComment.objects(id=recomment_id, writer=User.objects.get(email=g.email)).update(is_deleted=True)
        comment = Comment.objects(id=comment_id).get()
        comment.update(num_recomment=comment.num_recomment - 1)
        return "", 200

    @route("/<recomment_id>/like", methods=["POST"])
    @doc(summary="대댓글 좋아요", description="대댓글 좋아요")
    @check_recomment
    @marshal_empty(code=200, description="대댓글 좋아요 성공")
    @marshal_with(ApiErrorSchema, code=400, description="already push like user")
    def recomment_like(self, board_id, post_id, comment_id, recomment_id):
        user = User.objects(email=g.email).get()
        if user not in ReComment.objects(id=recomment_id).get().like:
            ReComment.objects(id=recomment_id).update_one(push__like=user)
        else:
            raise ApiError(message="좋아요를 이미 누른 유저입니다.", status_code=400)
        return "", 200


    @route("/<recomment_id>/like_cancel", methods=["POST"])
    @doc(summary="대댓글 좋아요 취소", description="대댓글 좋아요 취소")
    @check_recomment
    @marshal_empty(code=200, description="대댓글 취소 성공")
    @marshal_with(ApiErrorSchema, code=400, description="no push like user")
    def recomment_like_cancel(self, board_id, post_id, comment_id, recomment_id):
        user = User.objects(email=g.email).get()
        if user not in ReComment.objects(id=recomment_id).get().like:
            raise ApiError(message="좋아요를 누르지 않은 유저입니다.", status_code=400)
        else:
            ReComment.objects(id=recomment_id).update_one(pull__like=user)
        return "", 200
