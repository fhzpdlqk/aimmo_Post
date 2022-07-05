from flask import Blueprint, jsonify, request
from aimmoPost.aimmoPost.models import User, Post, Comment
from aimmoPost.aimmoPost.config import default
import mongoengine
import sys
import jwt
import json
from flask_classful import FlaskView, route

token_key = default.token


class ReCommentView(FlaskView):
    """
        대댓글 등록 API
        method: POST
        content-type: application/json
        url : /recomment/regist/:comment_id
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

    @route("/regist/<comment_id>", methods=["POST"])
    def recomment_regist(self, comment_id):
        try:
            decoded = jwt.decode(request.headers["Token"], token_key, algorithms="HS256")
            data = request.json
            if "content" in data and data["content"] == "":
                return jsonify({"success": False}), 400
            elif "content" not in data:
                return jsonify({"success": False}), 400
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

    """
        대댓글 수정 API
        method: PUT
        content-type: application/json
        url : /recomment/:recomment_id
        header: {
            token : 유저 정보 토큰
        }
        request : {
            content: string
        }
        parameter : {
            recomment_id: string
        }
        response : {
            성공시 : {success: true}, 200
            댓글 아이디가 누락되었을 경우: {"success": False, "message": "Please input id params"}: 400
            댓글 내용이 누락되었을 경우: {"success": False, "message": "내용이 누락되었습니다."}, 400
            아이디가 유효하지 않을 경우: {"success": False, "message": "유효하지 않은 아이디입니다."}: 401
            작성자 아이디가 아닐 경우 : {"success": False, "message": "작성자 아이디가 아닙니다."}, 401
            댓글 아이디가 존재하지 않을 경우: {"success": False, "message": "댓글 아이디가 존재하지 않습니다"}, 404
            이외의 오류가 발생했을 경우 :{success: false, message: error.message}, 500
        }
        """

    @route("/<recomment_id>", methods=["PUT"])
    def recomment_update(self, recomment_id):
        try:
            decoded = jwt.decode(request.headers["Token"], token_key, algorithms="HS256")
            data = request.json
            if "content" in data and data["content"] == "":
                return jsonify({"success": False, "message": "내용이 누락되었습니다."}), 400
            elif "content" not in data:
                return jsonify({"success": False, "message": "내용이 누락되었습니다."}), 400
            id = recomment_id
            user_id = decoded["user_id"]
            content = data["content"]
            result = Comment.ReComment.objects(id=id, writer=user_id).update(content=content)
            if result == 1:
                return jsonify({"success": True}), 200
            else:
                return jsonify({"success": False, "message": "작성자 아이디가 아닙니다."}), 401
        except jwt.exceptions.InvalidSignatureError:
            return jsonify({"success": False, "message": "유효하지 않은 아이디입니다."}), 401
        except mongoengine.errors.ValidationError:
            return jsonify({"success": False, "message": "댓글 아이디가 존재하지 않습니다"}), 404
        except:
            return jsonify({"success": False, "message": str(sys.exc_info()[0])}), 500

    """
        대댓글 삭제 API
        method: DELETE
        content-type: application/json
        url : /comment/?:recomment_id
        header: {
            token : 유저 정보 토큰
        }
        request : {

        }
        parameter : {
            recomment_id: string
        }
        response : {
            성공시 : {success: true}, 200
            댓글 아이디가 누락되었을 경우: {"success": False, "message": "Please input id params"}: 400
            아이디가 유효하지 않을 경우: {"success": False, "message": "유효하지 않은 아이디입니다."}, 401
            작성자 아이디가 아닐 경우: {"success": False, "message": "작성자 아이디가 아닙니다."}, 401
            댓글 아이디가 존재하지 않을 경우: {"success": False, "message": "댓글 아이디가 존재하지 않습니다"}, 404
            이외의 오류가 발생했을 경우 :{success: false, message: error.message}, 500
        }
    """

    @route("/<recomment_id>", methods=["DELETE"])
    def comment_delete(self, recomment_id):
        try:
            decoded = jwt.decode(request.headers["Token"], token_key, algorithms="HS256")
            id = recomment_id
            user_id = decoded["user_id"]
            result = Comment.ReComment.objects(id=id, writer=user_id).delete()
            if result == 1:
                return jsonify({"success": True})
            else:
                return jsonify({"success": False, "message": "작성자 아이디가 아닙니다."}), 401
        except jwt.exceptions.InvalidSignatureError:
            return jsonify({"success": False, "message": "유효하지 않은 아이디입니다."}), 401
        except mongoengine.errors.ValidationError:
            return jsonify({"success": False, "message": "대댓글 아이디가 존재하지 않습니다"}), 404
        except:
            return jsonify({"success": False, "message": str(sys.exc_info()[0])}), 500

    """
        대댓글 좋아요 API
        method: POST
        content-type: application/json
        url : /recomment/like/?:recomment_id
        header: {
            token : 유저 정보 토큰
        }
        request : {
        }
        parameter : {
            recomment_id: string
        }
        response : {
            성공시 : {success: true}, 200
            대댓글 아이디가 입력되지 않았을 경우 : {"success": false, "message": "please input id params"}, 400
            대댓글 아이디가 잘못되었을 경우: {"success": false, "message": "대댓글 아이디가 존재하지 않습니다."}, 404
            유저 아이디 토큰이 잘못되었을 경우 : {"success": false, "message": "유효하지 않은 아이디입니다."}, 401
            이미 좋아요를 누른 유저일 경우 : {"success": true}, 200
            이외의 오류가 발생했을 경우 : {"success": false, "message": error.message} 500
        }
    """

    @route("/like/<recomment_id>", methods=["POST"])
    def recomment_like(self, recomment_id):
        try:
            decoded = jwt.decode(request.headers["Token"], token_key, algorithms="HS256")
            id = recomment_id
            user_id = decoded["user_id"]
            user = User.User.objects(user_id=user_id)[0]
            if user not in Comment.ReComment.objects(id=id)[0].like:
                result = Comment.ReComment.objects(id=id).update_one(push__like=user)
            else:
                result = Comment.ReComment.objects(id=id).update_one(pull__like=user)
            if result == 1:
                return jsonify({"success": True}), 200
        except jwt.exceptions.InvalidSignatureError:
            return jsonify({"success": False, "message": "유효하지 않은 아이디입니다."}), 401
        except mongoengine.errors.ValidationError:
            return jsonify({"success": False, "message": "대댓글 아이디가 존재하지 않습니다"}), 404
        except:
            return jsonify({"success": False, "message": str(sys.exc_info()[0])}), 500
