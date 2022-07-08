from flask import jsonify
from flask_classful import FlaskView, route
from app.schemas.PostSchema import PostListSchema
from app.models import Post

class MainPageView(FlaskView):
    @route("/recent", methods=["GET"])
    def recent_post(self):
        post_list = Post.objects().order_by("-date")[:10]
        return jsonify(message=PostListSchema(many=True).dump(post_list)), 200

    @route("/comment", methods=["GET"])
    def comment_post(self):
        post_list = Post.objects().order_by("-num_comment")[:10]
        return jsonify(message=PostListSchema(many=True).dump(post_list)), 200

    @route("/like", methods=["GET"])
    def like_post(self):
        post_list = Post.objects().order_by("-like")[:10]
        return jsonify(message=PostListSchema(many=True).dump(post_list)), 200
