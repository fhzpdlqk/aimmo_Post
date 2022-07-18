import marshmallow
from bson import ObjectId
from flask_classful import FlaskView, route
from flask import request, g
from flask_apispec import marshal_with, use_kwargs
from app.models import Comment, User, Post
from app.schemas.CommentSchema import CommentSchema
from app.decorator import login_required, check_post, check_board, check_comment, check_comment_writer
from app.errors import ApiError, ApiErrorSchema

class CommentView(FlaskView):
    @route('/', methods=["POST"])
    @login_required
    @check_board
    @check_post
    @use_kwargs(CommentSchema(), locations=('json',))
    @marshal_with(ApiErrorSchema, code=422, description="validation error")
    def post(self, board_id, post_id, comment):
        """ write comment
            ---
            summary: 댓글 작성 기능
            description: 댓글 작성 기능
            tags: [comments]
            security:
                Authorization: []
            parameters:
                board_id: []
                post_id: []
            requestBody:
                required: true
                content:
                    application/json:
                        schema: CommentSchema
            responses:
                200:
                    description: no return
                401:
                    description: not login user or not valid token
                    content:
                        application/json:
                            schema: ApiErrorSchema
                404:
                    description: not found board id or post id
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
    @use_kwargs(CommentSchema(), locations=('json',))
    def put(self, board_id,post_id,comment_id, comment):
        """ update comment
            ---
            summary: 댓글 수정 기능
            description: 댓글 수정 기능
            tags: [comments]
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
                        schema: CommentSchema
            responses:
                200:
                    description: no return
                401:
                    description: not login user or not valid token
                    content:
                        application/json:
                            schema: ApiErrorSchema
                404:
                    description: not found board id or post id or comment id
                    content:
                        application/json:
                            schema: ApiErrorSchema
                422:
                    description: validation error
                    content:
                        application/json:
                            schema: ApiErrorSchema
        """
        Comment.objects(id=comment_id, writer=g.user_id).update(**request.json)
        return "", 200

    @route("/<string:comment_id>", methods=["DELETE"])
    @login_required
    @check_board
    @check_post
    @check_comment_writer
    def delete(self, board_id, post_id, comment_id):
        """ delete comment
            ---
            summary: 댓글 삭제 기능
            description: 댓글 삭제 기능
            tags: [comments]
            security:
                Authorization: []
            parameters:
                board_id: []
                post_id: []
                comment_id: []
            responses:
                200:
                    description: no return
                401:
                    description: not login user or not valid token
                    content:
                        application/json:
                            schema: ApiErrorSchema
                404:
                    description: not found board id or post id or comment id
                    content:
                        application/json:
                            schema: ApiErrorSchema
                422:
                    description: validation error
                    content:
                        application/json:
                            schema: ApiErrorSchema
        """
        Comment.objects(id=comment_id, writer=g.user_id).update(is_deleted=True)
        post = Post.objects(id=post_id).get()
        post.update(num_comment=post.num_comment - 1)
        return "", 200


    @route("/<string:comment_id>/like", methods=["POST"])
    @login_required
    @check_board
    @check_post
    @check_comment
    def like(self, board_id, post_id, comment_id):
        """ like comment
            ---
            summary: 댓글 좋아요 기능
            description: 댓글 좋아요 기능
            tags: [comments]
            security:
                Authorization: []
            parameters:
                board_id: []
                post_id: []
                comment_id: []
            responses:
                200:
                    description: no return
                401:
                    description: not login user or not valid token
                    content:
                        application/json:
                            schema: ApiErrorSchema
                404:
                    description: not found board id or post id or comment id
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
        if user not in Comment.objects(id=comment_id).get().like:
            Comment.objects(id=comment_id).update_one(push__like=user)
        else:
            Comment.objects(id=comment_id).update_one(pull__like=user)
        return "", 200
