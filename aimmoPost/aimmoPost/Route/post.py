from flask import Blueprint, jsonify, request
from aimmoPost.aimmoPost.models import User, Post, Comment
from aimmoPost.aimmoPost.models.User import UserSchema
from aimmoPost.aimmoPost.models.Post import PostListSchema, PostRegistSchema, PostDetailSchema
from aimmoPost.aimmoPost.models.Board import Board
from aimmoPost.aimmoPost.config import default
import mongoengine
import sys
import jwt
import json
from flask_classful import FlaskView, route

token_key = default.token


class PostView(FlaskView):

    """
    개시물 등록 API
    method: POST
    content-type: application/json
    uri: "/post/regist"
    header: {
        token : 유저 정보 토큰
    }
    request : {
        title: 제목 : String
        content: 내용 : String
        tag: 태그 : List
        notice: 공지사항 여부 : Boolean
    }
    response : {
        성공시 : {success: true}, 200
        제목, 내용이 누락되었을 경우 : {success: false,message:"제목/내용을 입력하세요"}, 400
        공지사항여부가 누락되었을 경우 : {success: false, message: "공지사항 여부를 입력해주세요"}, 400
        아이디가 잘못 입력되었을 경우 :{success: false, message: "아이디 토큰이 잘못되었습니다"}, 401
        이외의 오류가 발생했을 경우 :{success: false, message: error.message},500
    }
    """

    @route("/regist/<board_id>", methods=["POST"])
    def regist(self, board_id):
        try:
            decoded = jwt.decode(request.headers["Token"], token_key, algorithms="HS256")
            data = request.json

            if "title" not in data or data["title"] == "":
                return jsonify({"success": False, "message": "제목을 입력하세요"}), 400
            if "content" not in data or data["content"] == "":
                return jsonify({"success": False, "message": "내용을 입력하세요"}), 400
            if "notice" not in data or data["notice"] == "":
                return jsonify({"success": False, "message": "공지사항 여부를 입력해주세요"}), 400

            post = PostRegistSchema().load(data)
            post.writer = decoded["user_id"]
            post.save()
            result = Board.objects(id=board_id).update_one(push__post=post)
            if result == 1:
                return jsonify({"success": True}), 200
            else:
                return jsonify({"success": False}), 400
        except jwt.exceptions.InvalidSignatureError:
            return {"success": False, "message": "아이디 토큰이 잘못되었습니다"}, 401
        except:
            return {"success": False, "message": str(sys.exc_info()[0])}, 500

    """
        게시물 리스트 조회 API
        method: GET
        content-type: application/json
        url : /post/list/?:page&:filter
        header: {
            token : 유저 정보 토큰
        }
        request : {
        }
        parameter : {
            page: number
            filter: string
        }
        response : {
            성공시 : {success: true}, 200
            페이지 인덱스가 음수일 경우: {"success": false, "message": "유효하지 않은 페이지 인덱스 입니다."}, 400
            이외의 오류가 발생했을 경우 :{success: false, message: error.message}, 500
        }
    """

    @route("/list/", methods=["GET"])
    def post_list(self):
        try:
            if "page" not in request.args:
                page = 1
            else:
                page = int(request.args["page"])
            if "filter" not in request.args:
                filter = "date"
            else:
                filter = request.args["filter"]
            if filter not in ["date", "comment", "like"]:
                filter = "date"

            datas = Post.Post.objects().order_by("-notice", "-" + filter)[(page - 1) * 10 : page * 10]
            result = []
            decoded = jwt.decode(request.headers["Token"], token_key, algorithms="HS256")
            user = User.User.objects(user_id=decoded["user_id"])
            if len(user) == 0:
                return jsonify({"success": False, "message": "유효하지 않은 아이디입니다."}), 401
            user = user[0]
            for data in datas:
                new_data = PostListSchema().dump(data)
                if user in data.like:
                    new_data["is_like"] = True
                else:
                    new_data["is_like"] = False
                result.append(new_data)
            return jsonify({"success": True, "message": result}), 200
        except IndexError:
            return jsonify({"success": False, "message": "유효하지 않은 페이지 인덱스 입니다."}), 400
        except:
            return jsonify({"success": False, "message": str(sys.exc_info())}), 500

    """
        게시물 상세 조회 API
        method: GET
        content-type: application/json
        url : /post/?:id
        header: {
            token : 유저 정보 토큰
        }
        request : {

        }
        parameter : {
            id: string
        }
        response : {
            성공시 : {success: true}, 200
            게시물 아이디가 입력되지 않았을 경우 : {"success": false, "message": "please input id params"}, 400
            게시물 아이디가 잘못되었을 경우: {"success": false, "message": "post_id를 찾을 수 없습니다"}, 404
            이외의 오류가 발생했을 경우 :{success: false, message: error.message}, 500
        }
    """

    @route("/<id>", methods=["GET"])
    def get_post_detail(self, id):
        try:
            data = Post.Post.objects(id=id)
            if len(data) == 0:
                return jsonify({"success": False, "message": "post_id를 찾을 수 없습니다"}), 404
            data = data[0]
            result = PostDetailSchema().dump(data)

            decoded = jwt.decode(request.headers["Token"], token_key, algorithms="HS256")
            user = User.User.objects(user_id=decoded["user_id"])
            if len(user) == 0:
                return jsonify({"success": False, "message": "유효하지 않은 아이디입니다."}), 401
            user = user[0]
            if user in result["like"]:
                result["is_like"] = True
            else:
                result["is_like"] = False
            del result["like"]

            for i in result["comment"]:
                i["is_like"] = user in i["like"]
                del i["like"]
                if "recomment" not in i:
                    i["recomment"] = []
                for j in i["recomment"]:
                    j["is_like"] = user in j["like"]
            return jsonify({"success": True, "message": result}), 200
        except mongoengine.errors.ValidationError:
            return jsonify({"success": False, "message": "post_id를 찾을 수 없습니다"}), 404
        except:
            print(sys.exc_info()[0])
            return jsonify({"success": False, "message": str(sys.exc_info())}), 500

    """
        게시물 삭제 API
        method: DELETE
        content-type: application/json
        url : /post/?:id
        header: {
            token : 유저 정보 토큰
        }
        request : {

        }
        parameter : {
            id: string
        }
        response : {
            성공시 : {success: true}, 200
            게시물 아이디가 입력되지 않았을 경우 : {"success": false, "message": "please input id params"}, 400
            게시물 아이디가 잘못되었을 경우: {"success": false, "message": "게시물 아이디가 존재하지 않습니다."}, 404
            유저 아이디가 잘못되었을 경우 : {"success": false, "message": "유효하지 않은 아이디입니다."}, 401
            유저 아이디가 다른 아이디일 경우 : {"success": false, "message": "작성자 아이디가 아닙니다."}, 401
            이외의 오류가 발생했을 경우 : {"success": false, "message": error.message} 500
        }
    """

    @route("/<id>", methods=["DELETE"])
    def delete_post_detail(self, id):
        try:
            decoded = jwt.decode(request.headers["Token"], token_key, algorithms="HS256")
            result = Post.Post.objects(id=id, writer=decoded["user_id"]).delete()
            if result == 1:
                return jsonify({"success": True}), 200
            else:
                return jsonify({"success": False, "message": "작성자 아이디가 아닙니다."}), 401
        except mongoengine.errors.ValidationError:
            return jsonify({"success": False, "message": "게시물 아이디가 존재하지 않습니다"}), 404
        except jwt.exceptions.InvalidSignatureError:
            return jsonify({"success": False, "message": "유효하지 않은 아이디입니다."}), 401
        except:
            return jsonify({"success": False, "message": str(sys.exc_info()[0])}), 500

    """
        게시물 수정 API
        method: PUT
        content-type: application/json
        url : /post/?:id
        header: {
            token : 유저 정보 토큰
        }
        request : {
            title: string,
            content: string,
            tag: list,
            notice: bool
        }
        parameter : {
            id: string
        }
        response : {
            성공시 : {success: true}, 200
            게시물 아이디가 입력되지 않았을 경우 : {"success": false, "message": "please input id params"}, 400
            게시물 아이디가 잘못되었을 경우: {"success": false, "message": "게시물 아이디가 존재하지 않습니다."}, 404
            유저 아이디 토큰이 잘못되었을 경우 : {"success": false, "message": "유효하지 않은 아이디입니다."}, 401
            유저 아이디가 다른 아이디일 경우 : {"success": false, "message": "작성자 아이디가 아닙니다."}, 401
            이외의 오류가 발생했을 경우 : {"success": false, "message": error.message} 500
        }
    """

    @route("/<id>", methods=["PUT"])
    def update_post_detail(self, id):
        try:
            decoded = jwt.decode(request.headers["Token"], token_key, algorithms="HS256")
            data = request.json
            if "title" in data and data["title"] == "":
                del data["title"]
            if "content" in data and data["content"] == "":
                del data["content"]
            if "notice" in data and data["notice"] == "":
                del data["notice"]
            result = Post.Post.objects(id=id, writer=decoded["user_id"]).update(**data)

            if result == 1:
                return jsonify({"success": True}), 200
            else:
                return jsonify({"success": False, "message": "작성자 아이디가 아닙니다."}), 401
        except jwt.exceptions.InvalidSignatureError:
            return jsonify({"success": False, "message": "유효하지 않은 아이디입니다."}), 401
        except mongoengine.errors.ValidationError:
            return jsonify({"success": False, "message": "게시물 아이디가 존재하지 않습니다"}), 404
        except:
            return jsonify({"success": False, "message": str(sys.exc_info()[0])}), 500

    """
        게시물 좋아요 API
        method: POST
        content-type: application/json
        url : /post/like/?:id
        header: {
            token : 유저 정보 토큰
        }
        request : {
        }
        parameter : {
            id: string
        }
        response : {
            성공시 : {success: true}, 200
            게시물 아이디가 입력되지 않았을 경우 : {"success": false, "message": "please input id params"}, 400
            게시물 아이디가 잘못되었을 경우: {"success": false, "message": "게시물 아이디가 존재하지 않습니다."}, 404
            유저 아이디 토큰이 잘못되었을 경우 : {"success": false, "message": "유효하지 않은 아이디입니다."}, 401
            이미 좋아요를 누른 유저일 경우 : {"success": true}, 200
            이외의 오류가 발생했을 경우 : {"success": false, "message": error.message} 500
        }
    """

    @route("/like/<id>", methods=["POST"])
    def post_like(self, id):
        try:
            decoded = jwt.decode(request.headers["Token"], token_key, algorithms="HS256")
            user = User.User.objects(user_id=decoded["user_id"])[0]
            if user not in Post.Post.objects(id=id)[0].like:
                result = Post.Post.objects(id=id).update_one(push__like=user)
            else:
                result = Post.Post.objects(id=id).update_one(pull__like=user)
            if result == 1:
                return jsonify({"success": True}), 200
        except jwt.exceptions.InvalidSignatureError:
            return jsonify({"success": False, "message": "유효하지 않은 아이디입니다."}), 401
        except mongoengine.errors.ValidationError:
            return jsonify({"success": False, "message": "게시물 아이디가 존재하지 않습니다"}), 404
        except:
            return jsonify({"success": False, "message": str(sys.exc_info()[0])}), 500
