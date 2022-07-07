from flask import Blueprint, jsonify, request
import mongoengine
import sys
import jwt
import json
from flask_classful import FlaskView, route
from aimmoPost.aimmoPost.models.Post import Post, PostListSchema
from aimmoPost.aimmoPost.models.Comment import Comment


class MainPageView(FlaskView):
    """
    메인페이지 게시물 최신 10개
    method: GET
    content-type: application/json
    uri: "/mainpage/recent"
    response : {
        성공시 : {success: true}, 200
    }
    """

    @route("/recent", methods=["GET"])
    def recent_post(self):
        post_list = Post.objects().order_by("-date")[:10]
        result = []
        for post in post_list:
            new_data = PostListSchema().dump(post)
            new_data["num_comment"] = len(Comment.objects(post=post.id))
            result.append(new_data)
        return jsonify({"success": True, "message": result}), 200

    """
        메인페이지 게시물 댓글순 10개
        method: GET
        content-type: application/json
        uri: "/mainpage/comment"
        response : {
            성공시 : {success: true}, 200
        }
    """

    @route("/comment", methods=["GET"])
    def comment_post(self):
        post_list = Post.objects()
        result = []
        for post in post_list:
            new_data = PostListSchema().dump(post)
            new_data["num_comment"] = len(Comment.objects(post=post.id))
            result.append(new_data)
        result.sort(key=lambda x: x["num_comment"], reverse=True)
        return jsonify({"success": True, "message": result}), 200

    """
        메인페이지 게시물 좋아요순 10개
        method: GET
        content-type: application/json
        uri: "/mainpage/comment"
        response : {
            성공시 : {success: true}, 200
        }
    """

    @route("/like", methods=["GET"])
    def like_post(self):
        post_list = Post.objects().order_by("-like")[:10]
        result = []
        for post in post_list:
            new_data = PostListSchema().dump(post)
            new_data["num_comment"] = len(Comment.objects(post=post.id))
            result.append(new_data)
        return jsonify({"success": True, "message": result}), 200