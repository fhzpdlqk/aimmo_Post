from flask import Blueprint, jsonify, request
from aimmoPost.aimmoPost.models import User, Post, Like, Comment
from aimmoPost.aimmoPost.config import default
import mongoengine
import sys
import jwt
import json
from flask_classful import FlaskView, route

token_key = default.token


class CommentView(FlaskView):
    """
    댓글 등록 API
    method: POST
    content-type: application/json
    url : /comment/regist?
    header: {
        token : 유저 정보 토큰
    }
    request : {
        content: string
    }
    parameter : {
        id: string
    }
    response : {
        status : 200, success: true
        status : 300, success: true
    }
    """

    @route("/regist", methods=["POST"])
    def comment_regist(self):
        try:
            decoded = jwt.decode(request.headers["Token"], token_key, algorithms="HS256")
            if "id" not in request.args:
                return jsonify({"success": False, "message": "Please input id params"})
            data = request.json
            id = request.args["id"]
            user_id = decoded["user_id"]
            content = data["content"]
            temp = Comment.Comment(writer=user_id, content=content).save()
            result = Post.Post.objects(id=id).update_one(push__comment=temp)
            if result == 1:
                return jsonify({"success": True})
            else:
                return jsonify({"success": False})
        except:
            return jsonify({"success": False, "message": str(sys.exc_info()[0])})

    """
        댓글 수정 API
        method: PUT
        content-type: application/json
        url : /comment/?
        header: {
            token : 유저 정보 토큰
        }
        request : {
            content: string
        }
        parameter : {
            comment_id: string
        }
        response : {
            status : 200, success: true
            status : 300, success: true
        }
    """

    @route("/", methods=["PUT"])
    def comment_update(self):
        try:
            decoded = jwt.decode(request.headers["Token"], token_key, algorithms="HS256")
            if "comment_id" not in request.args:
                return jsonify({"success": False, "message": "Please input id params"})
            data = request.json
            id = request.args["comment_id"]
            user_id = decoded["user_id"]
            content = data["content"]
            result = Comment.Comment(id=id, writer=user_id).update(content=content)
            if result == 1:
                return jsonify({"success": True})
            else:
                return jsonify({"success": False})
        except:
            return jsonify({"success": False, "message": str(sys.exc_info()[0])})

    @route("/", methods=["DELETE"])
    def comment_delete(self):
        try:
            decoded = jwt.decode(request.headers["Token"], token_key, algorithms="HS256")
            if "comment_id" not in request.args:
                return jsonify({"success": False, "message": "Please input id params"})
            id = request.args["comment_id"]
            user_id = decoded["user_id"]
            result = Comment.Comment.objects(id=id, writer=user_id).delete()
            if result == 1:
                return jsonify({"success": True})
            else:
                return jsonify({"success": False})
        except:
            return jsonify({"success": False, "message": str(sys.exc_info()[0])})
