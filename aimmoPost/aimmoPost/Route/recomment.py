from flask import Blueprint, jsonify, request
from aimmoPost.aimmoPost.models import User, Post, Like, Comment
from aimmoPost.aimmoPost.config import default
import mongoengine
import sys
import jwt
import json
from flask_classful import FlaskView, route

token_key = default.token


class ReCommentView(FlaskView):
    @route("/regist", methods=["POST"])
    def recomment_regist(self):
        try:
            decoded = jwt.decode(request.headers["Token"], token_key, algorithms="HS256")
            if "comment_id" not in request.args:
                return jsonify({"success": False, "message": "Please input id params"}), 400
            data = request.json
            if "content" in data and data["content"] == "":
                return jsonify({"success": False}), 400
            elif "content" not in data:
                return jsonify({"success": False}), 400
            comment_id = request.args["comment_id"]
            user_id = decoded["user_id"]
            content = data["content"]
            temp = Comment.ReComment(writer=user_id, content=content).save()
            result = Comment.Comment.objects(id=comment_id).update_one(push__re_comment=temp)
            if result == 1:
                return jsonify({"success": True}), 200
            else:
                return jsonify({"success": False}), 400
        except jwt.exceptions.InvalidSignatureError:
            return jsonify({"success": False, "message": "유효하지 않은 아이디입니다."}), 401
        except mongoengine.errors.ValidationError:
            return jsonify({"success": False, "message": "게시물 아이디가 존재하지 않습니다"}), 404
        except:
            return jsonify({"success": False, "message": str(sys.exc_info()[0])}), 500
