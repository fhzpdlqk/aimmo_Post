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
    url : /comment/regist?:id
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
        성공시 : {success: true}, 200
        게시물 아이디가 누락되었을 경우: {"success": False, "message": "Please input id params"}: 400
        댓글 내용이 누락되었을 경우: {"success": False, "message": "내용이 누락되었습니다."}, 400
        아이디가 유효하지 않을 경우: {"success": False, "message": "유효하지 않은 아이디입니다."}: 401
        게시물 아이디가 존재하지 않을 경우: {"success": False, "message": "게시물 아이디가 존재하지 않습니다"}, 404
        이외의 오류가 발생했을 경우 :{success: false, message: error.message}, 500
    }
    """

    @route("/regist", methods=["POST"])
    def comment_regist(self):
        try:
            decoded = jwt.decode(request.headers["Token"], token_key, algorithms="HS256")
            if "id" not in request.args and "comment_id" not in request.args:
                return jsonify({"success": False, "message": "Please input id params"}), 400
            data = request.json
            if "content" in data and data["content"] == "":
                return jsonify({"success": False, "message": "내용이 누락되었습니다."}), 400
            elif "content" not in data:
                return jsonify({"success": False, "message": "내용이 누락되었습니다."}), 400
            id = request.args["id"]
            user_id = decoded["user_id"]
            content = data["content"]
            temp = Comment.Comment(writer=user_id, content=content).save()
            result = Post.Post.objects(id=id).update_one(push__comment=temp)
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

    """
        댓글 수정 API
        method: PUT
        content-type: application/json
        url : /comment/?:comment_id
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
        성공시 : {success: true}, 200
        댓글 아이디가 누락되었을 경우: {"success": False, "message": "Please input id params"}: 400
        댓글 내용이 누락되었을 경우: {"success": False, "message": "내용이 누락되었습니다."}, 400
        아이디가 유효하지 않을 경우: {"success": False, "message": "유효하지 않은 아이디입니다."}: 401
        댓글 아이디가 존재하지 않을 경우: {"success": False, "message": "댓글 아이디가 존재하지 않습니다"}, 404
        이외의 오류가 발생했을 경우 :{success: false, message: error.message}, 500
    }
    """

    @route("/", methods=["PUT"])
    def comment_update(self):
        try:
            decoded = jwt.decode(request.headers["Token"], token_key, algorithms="HS256")
            if "comment_id" not in request.args:
                return jsonify({"success": False, "message": "Please input id params"}), 400
            data = request.json
            if "content" in data and data["content"] == "":
                return jsonify({"success": False}), 400
            elif "content" not in data:
                return jsonify({"success": False}), 400
            id = request.args["comment_id"]
            user_id = decoded["user_id"]
            content = data["content"]
            result = Comment.Comment(id=id, writer=user_id).update(content=content)
            if result == 1:
                return jsonify({"success": True}), 200
            else:
                return jsonify({"success": False})
        except jwt.exceptions.InvalidSignatureError:
            return jsonify({"success": False, "message": "유효하지 않은 아이디입니다."}), 401
        except mongoengine.errors.ValidationError:
            return jsonify({"success": False, "message": "댓글 아이디가 존재하지 않습니다"}), 404
        except:
            return jsonify({"success": False, "message": str(sys.exc_info()[0])}), 500

    """
        댓글 수정 API
        method: DELETE
        content-type: application/json
        url : /comment/?:comment_id
        header: {
            token : 유저 정보 토큰
        }
        request : {

        }
        parameter : {
            comment_id: string
        }
        response : {
            성공시 : {success: true}, 200
            댓글 아이디가 누락되었을 경우: {"success": False, "message": "Please input id params"}: 400
            아이디가 유효하지 않을 경우: {"success": False, "message": "유효하지 않은 아이디입니다."}: 401
            댓글 아이디가 존재하지 않을 경우: {"success": False, "message": "댓글 아이디가 존재하지 않습니다"}, 404
            이외의 오류가 발생했을 경우 :{success: false, message: error.message}, 500
        }
    """

    @route("/", methods=["DELETE"])
    def comment_delete(self):
        try:
            decoded = jwt.decode(request.headers["Token"], token_key, algorithms="HS256")
            if "comment_id" not in request.args:
                return jsonify({"success": False, "message": "Please input id params"}), 400
            id = request.args["comment_id"]
            user_id = decoded["user_id"]
            result = Comment.Comment.objects(id=id, writer=user_id).delete()
            if result == 1:
                return jsonify({"success": True})
            else:
                return jsonify({"success": False})
        except jwt.exceptions.InvalidSignatureError:
            return jsonify({"success": False, "message": "유효하지 않은 아이디입니다."}), 401
        except mongoengine.errors.ValidationError:
            return jsonify({"success": False, "message": "댓글 아이디가 존재하지 않습니다"}), 404
        except:
            return jsonify({"success": False, "message": str(sys.exc_info()[0])}), 500
