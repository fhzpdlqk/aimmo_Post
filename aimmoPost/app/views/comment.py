import marshmallow
from bson import ObjectId
from flask_classful import FlaskView, route
from flask import jsonify, request, g
from app.models import Comment, User
from app.schemas.CommentSchema import CommentRegistSchema
from app.decorator import login_required, check_post, check_board, check_comment, check_comment_writer

class CommentView(FlaskView):
    @login_required
    @check_board
    @check_post
    def post(self, board_id, post_id):
        try:
            comment = CommentRegistSchema().load(request.json)
            comment.writer = g.user_id
            comment.post = ObjectId(post_id)
            comment.save()
            return "", 200
        except marshmallow.exceptions.ValidationError as err:
            return jsonify({"message": err.messages}), 422

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
