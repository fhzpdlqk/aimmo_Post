from flask import request, g
import marshmallow
from bson import ObjectId
from flask_classful import FlaskView, route
from flask_apispec import use_kwargs, marshal_with
from app.models import ReComment, User, Comment
from app.schemas.ReCommentSchema import ReCommentSchema
from app.decorator import login_required, check_board, check_post, check_comment, check_recomment_writer, check_recomment
from app.errors import ApiError, ApiErrorSchema

class ReCommentView(FlaskView):
    @route("/",methods=["POST"])
    @login_required
    @check_board
    @check_post
    @check_comment
    @use_kwargs(ReCommentSchema, locations=('json',))
    @marshal_with(ApiErrorSchema, code=422, description='validation error')
    def post(self, board_id, post_id, comment_id, recomment):
        """ write re_comment
            ---
            summary: 대댓글 작성 기능
            description: 대댓글 작성 기능
            tags: [recomments]
            security:
                Authorization: []
            parameters:
                board_id: []
                post_id: []
                comment_id: []
            requestBody:
                required: true
                content:
                    application/json:
                        schema: ReCommentSchema
            responses:
                200:
                    description: no return
                401:
                    description: not login user or not valid token
                    content:
                        application/json:
                            schema: ApiErrorSchema
                404:
                    description: not found board id or post id or commentid
                    content:
                        application/json:
                            schema: ApiErrorSchema
                422:
                    description: validation error
                    content:
                        application/json:
                            schema: ApiErrorSchema
        """
        try:
            recomment.writer = g.user_id
            recomment.comment = ObjectId(comment_id)
            recomment.save()
            comment = Comment.objects(id=comment_id).get()
            comment.update(num_recomment=comment.num_recomment + 1)
            return "", 200
        except marshmallow.exceptions.ValidationError as err:
            return ApiError(message=err.messages), 422

    @route("/<recomment_id>", methods=["PUT"])
    @login_required
    @check_board
    @check_post
    @check_comment
    @check_recomment_writer
    @use_kwargs(ReCommentSchema, locations=('json',))
    def put(self, board_id, post_id, comment_id, recomment_id, recomment):
        """ update re_comment
            ---
            summary: 대댓글 수정 기능
            description: 대댓글 수정 기능
            tags: [recomments]
            security:
                Authorization: []
            parameters:
                board_id: []
                post_id: []
                comment_id: []
                recomment_id: []
            requestBody:
                required: true
                content:
                    application/json:
                        schema: ReCommentSchema
            responses:
                200:
                    description: no return
                401:
                    description: not login user or not valid token
                    content:
                        application/json:
                            schema: ApiErrorSchema
                404:
                    description: not found board id or post id or comment id, recomment id
                    content:
                        application/json:
                            schema: ApiErrorSchema
                422:
                    description: validation error
                    content:
                        application/json:
                            schema: ApiErrorSchema
        """
        ReComment.objects(id=recomment_id, writer=g.user_id).update(**request.json)
        return "", 200

    @route("/<recomment_id>", methods=["DELETE"])
    @login_required
    @check_board
    @check_post
    @check_comment
    @check_recomment_writer
    def delete(self, board_id, post_id, comment_id, recomment_id):
        """ delete re_comment
            ---
            summary: 대댓글 삭제 기능
            description: 대댓글 삭제 기능
            tags: [recomments]
            security:
                Authorization: []
            parameters:
                board_id: []
                post_id: []
                comment_id: []
                recomment_id: []
            responses:
                200:
                    description: no return
                401:
                    description: not login user or not valid token
                    content:
                        application/json:
                            schema: ApiErrorSchema
                404:
                    description: not found board id or post id or comment id, recomment id
                    content:
                        application/json:
                            schema: ApiErrorSchema
                422:
                    description: validation error
                    content:
                        application/json:
                            schema: ApiErrorSchema
        """
        ReComment.objects(id=recomment_id, writer=g.user_id).update(is_deleted=True)
        comment = Comment.objects(id=comment_id).get()
        comment.update(num_recomment=comment.num_recomment - 1)
        return "", 200

    @route("/<recomment_id>/like", methods=["POST"])
    @login_required
    @check_board
    @check_post
    @check_comment
    @check_recomment
    def recomment_like(self, board_id, post_id, comment_id, recomment_id):
        """ like re_comment
            ---
            summary: 대댓글 좋아요 기능
            description: 대댓글 좋아요 기능
            tags: [recomments]
            security:
                Authorization: []
            parameters:
                board_id: []
                post_id: []
                comment_id: []
                recomment_id: []
            responses:
                200:
                    description: no return
                401:
                    description: not login user or not valid token
                    content:
                        application/json:
                            schema: ApiErrorSchema
                404:
                    description: not found board id or post id or comment id, recomment id
                    content:
                        application/json:
                            schema: ApiErrorSchema
                422:
                    description: validation error
                    content:
                        application/json:
                            schema: ApiErrorSchema
        """
        user = User.objects(user_id=g.user_id).get()
        if user not in ReComment.objects(id=recomment_id).get().like:
            ReComment.objects(id=recomment_id).update_one(push__like=user)
        else:
            ReComment.objects(id=recomment_id).update_one(pull__like=user)
        return "", 200
