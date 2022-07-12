from flask import jsonify, request, g
import marshmallow
from bson import ObjectId
from flask_classful import FlaskView, route
from app.models import ReComment, User, Comment
from app.schemas.ReCommentSchema import ReCommentRegistSchema
from app.decorator import login_required, check_board, check_post, check_comment, check_recomment_writer, check_recomment


class ReCommentView(FlaskView):
    @login_required
    @check_board
    @check_post
    @check_comment
    def post(self, board_id, post_id, comment_id):
        try:
            recomment = ReCommentRegistSchema().load(request.json)
            recomment.writer = g.user_id
            recomment.comment = ObjectId(comment_id)
            recomment.save()
            comment = Comment.objects(id=comment_id).get()
            comment.update(num_recomment=comment.num_recomment + 1)
            return "", 200
        except marshmallow.exceptions.ValidationError as err:
            return jsonify({"message": err.messages}), 422

    @route("/<recomment_id>", methods=["PUT"])
    @login_required
    @check_board
    @check_post
    @check_comment
    @check_recomment_writer
    def put(self, board_id, post_id, comment_id, recomment_id):
        ReComment.objects(id=recomment_id, writer=g.user_id).update(**request.json)
        return "", 200

    @route("/<recomment_id>", methods=["DELETE"])
    @login_required
    @check_board
    @check_post
    @check_comment
    @check_recomment_writer
    def delete(self, board_id, post_id, comment_id, recomment_id):
        ReComment.objects(id=recomment_id, writer=g.user_id).delete()
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
        user = User.objects(user_id=g.user_id).get()
        if user not in ReComment.objects(id=recomment_id).get().like:
            ReComment.objects(id=recomment_id).update_one(push__like=user)
        else:
            print("aa")
            ReComment.objects(id=recomment_id).update_one(pull__like=user)
        return "", 200
