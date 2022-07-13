import marshmallow
from bson import ObjectId
from flask_classful import FlaskView, route
from flask import g, jsonify, request
from app.schemas.PostSchema import PostListSchema, PostRegistSchema, PostDetailSchema
from app.models import Post, User
from app.decorator import login_required,check_board, check_post, check_post_writer

class PostView(FlaskView):
    @login_required
    @check_board
    def post(self, board_id):
        try:
            post = PostRegistSchema().load(request.json)
            post.writer = g.user_id
            post.board = ObjectId(board_id)
            post.save()
            return "", 200
        except marshmallow.exceptions.ValidationError as err:
            return jsonify({"message": err.messages}), 422

    @route("/<string:post_id>", methods=["GET"])
    @login_required
    @check_board
    @check_post
    def get(self, board_id, post_id):
        post = Post.objects(board=board_id, id=post_id).get()
        return PostDetailSchema().dump(post), 200

    @route("/<string:post_id>", methods=["DELETE"])
    @login_required
    @check_board
    @check_post_writer
    def delete(self, board_id, post_id):
        Post.objects(id=post_id, writer=g.user_id).delete()
        return "", 200

    @route("/<string:post_id>", methods=["PUT"])
    @login_required
    @check_board
    @check_post_writer
    def put(self, board_id, post_id):
        try:
            Post.objects(id=post_id, writer=g.user_id).update(**request.json)
            return "", 200
        except marshmallow.exceptions.ValidationError as err:
            return jsonify({"message": err.messages}), 422


    @route("/<string:post_id>/like", methods=["POST"])
    @login_required
    @check_board
    @check_post
    def like(self, board_id, post_id):
        user = User.objects(user_id=g.user_id).get()
        if user not in Post.objects(id=post_id).get().like:
            Post.objects(id=post_id).update_one(push__like=user)
        else:
            Post.objects(id=post_id).update_one(pull__like=user)
        return "", 200


    @route("/search", methods=["POST"])
    @check_board
    def post_search(self, board_id):
        posts = Post.objects(board=board_id, __raw__={"$or": [{"content": {"$regex": request.json["search_word"]}}, {"title": {"$regex": request.json["search_word"]}}]})
        return jsonify(post_list=PostListSchema(many=True).dump(posts)),200

    @route("/", methods=["GET"])
    @login_required
    @check_board
    def get_post_list(self, board_id):
        try:
            params = request.args.to_dict()
            if "page" not in params:
                params["page"] = "1"
            if "size" not in params:
                params["size"] = "10"
            posts = Post.objects(board=board_id).order_by("-notice")[(int(params["page"]) - 1) * int(params["size"]): int(params["page"]) * int(params["size"])]
            result = []
            for post in posts:
                new_data = PostListSchema().dump(post)
                new_data["is_like"] = User.objects(user_id=g.user_id).get() in post.like
                result.append(new_data)
            return jsonify(post_list=result), 200
        except IndexError:
            return jsonify(message="유효하지 않은 페이지 인덱스 입니다."), 404
