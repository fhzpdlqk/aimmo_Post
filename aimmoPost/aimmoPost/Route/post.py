from flask import Blueprint, jsonify, request
from aimmoPost.aimmoPost.models import User, Post, Like, Comment
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

    @route("/regist", methods=["POST"])
    def regist(self):
        try:
            decoded = jwt.decode(request.headers["Token"], token_key, algorithms="HS256")
            data = request.json

            if "title" not in data or data["title"] == "":
                return jsonify({"success": False, "message": "제목을 입력하세요"}), 400
            if "content" not in data or data["content"] == "":
                return jsonify({"success": False, "message": "내용을 입력하세요"}), 400
            if "notice" not in data or data["notice"] == "":
                return jsonify({"success": False, "message": "공지사항 여부를 입력해주세요"}), 400
            user_id = decoded["user_id"]
            title = data["title"]
            content = data["content"]
            if "tag" in data:
                tag = data["tag"]
            else:
                tag = []
            notice = data["notice"]
            Post.Post(writer=user_id, title=title, content=content, tag=tag, notice=notice).save()
            return jsonify({"success": True}), 200
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
            parameter_dic = request.args.to_dict()
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
            for data in datas:
                new_data = {}
                new_data["id"] = str(data.id)
                new_data["writer"] = data.writer
                new_data["date"] = data.date
                new_data["title"] = data.title
                new_data["tag"] = data.tag
                new_data["notice"] = data.notice
                new_data["num_like"] = len(data.like)
                new_data["num_comment"] = len(data.comment)
                result.append(new_data)
            return jsonify({"success": True, "message": result}), 200

            # return jsonify({"success": True, "message": json.loads(datas.to_json())})
        except IndexError:
            return jsonify({"success": False, "message": "유효하지 않은 페이지 인덱스 입니다."}), 400
        except:
            print(str(sys.exc_info()))
            return jsonify({"success": False, "message": str(sys.exc_info()[0])}), 500

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

    @route("/", methods=["GET"])
    def get_post_detail(self):
        try:
            if "id" not in request.args:
                return jsonify({"success": False, "message": "Please input id params"}), 400
            id = request.args["id"]
            data = Post.Post.objects(id=id)

            result = {}
            result["id"] = str(data[0].id)
            result["content"] = data[0].content
            result["title"] = data[0].title
            result["writer"] = data[0].writer
            result["notice"] = data[0].notice
            result["num_like"] = len(data[0].like)
            result["num_comment"] = len(data[0].comment)
            result["tag"] = data[0].tag
            result["date"] = data[0].date
            result["comment"] = []

            for i in data[0].comment:
                new_comment_data = {}
                new_comment_data["id"] = str(i.id)
                new_comment_data["writer"] = i.writer
                new_comment_data["date"] = i.date
                new_comment_data["num_like"] = len(i.like)
                new_comment_data["content"] = i.content
                new_comment_data["re_comment"] = []

                for j in i.re_comment:
                    new_recomment_data = {}
                    new_recomment_data["id"] = str(j.id)
                    new_recomment_data["writer"] = j.writer
                    new_recomment_data["date"] = j.date
                    new_recomment_data["num_like"] = len(j.like)
                    new_recomment_data["content"] = j.content
                    new_comment_data["re_comment"].append(new_recomment_data)
                result["comment"].append(new_comment_data)
            return jsonify({"success": True, "message": result}), 200
        except mongoengine.errors.ValidationError:
            return jsonify({"success": False, "message": "post_id를 찾을 수 없습니다"}), 404
        except:
            print(sys.exc_info()[0])
            return jsonify({"success": False, "message": str(sys.exc_info()[0])}), 500

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

    @route("/", methods=["DELETE"])
    def delete_post_detail(self):
        try:
            decoded = jwt.decode(request.headers["Token"], token_key, algorithms="HS256")
            if "id" not in request.args:
                return jsonify({"success": False, "message": "please input id params"}), 400
            id = request.args["id"]
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

    @route("/", methods=["PUT"])
    def update_post_detail(self):
        try:
            decoded = jwt.decode(request.headers["Token"], token_key, algorithms="HS256")
            if "id" not in request.args:
                return jsonify({"success": False, "message": "please input id params"}), 400
            id = request.args["id"]
            user_id = decoded["user_id"]
            data = request.json
            if "title" in data and data["title"] == "":
                del data["title"]
            if "content" in data and data["content"] == "":
                del data["content"]
            if "notice" in data and data["notice"] == "":
                del data["notice"]
            result = Post.Post.objects(id=id, writer=user_id).update(**data)

            if result == 1:
                return jsonify({"success": True}), 200
            else:
                return jsonify({"success": False, "message": "작성자 아이디가 아닙니다."}), 401
        except jwt.exceptions.InvalidSignatureError:
            return jsonify({"success": False, "message": "유효하지 않은 아이디입니다."}), 401
        except mongoengine.errors.ValidationError:
            return jsonify({"success": False, "message": "게시물 아이디가 존재하지 않습니다"}), 404
        except:
            print(str(sys.exc_info()[0]))
            return jsonify({"success": False, "message": str(sys.exc_info()[0])}), 500
