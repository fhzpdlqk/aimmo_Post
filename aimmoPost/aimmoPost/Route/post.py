from flask import Blueprint, jsonify, request
from aimmoPost.aimmoPost.models import User, Post, Like, Comment
from aimmoPost.aimmoPost.config import default
import mongoengine
import sys
import jwt
import json

post = Blueprint("post", __name__, url_prefix="/post")
token_key = default.token

"""
    개시물 등록 API
    method: POST
    content-type: application/json
    url: /post/regist
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
        status : 200, success: true
        status : 300, success: true
    }
"""


@post.route("/regist", methods=["POST"])
def regist():
    try:
        decoded = jwt.decode(request.headers["Token"], token_key, algorithms="HS256")
        data = request.json
        user_id = decoded["user_id"]
        title = data["title"]
        content = data["content"]
        if "tag" in data:
            tag = data["tag"]
        else:
            tag = []
        notice = data["notice"]
        Post.Post(writer=user_id, title=title, content=content, tag=tag, notice=notice).save()
        return jsonify({"success": True})
    except:
        return jsonify({"success": False, "message": str(sys.exc_info()[0])})


"""
    게시물 리스트 조회 API
    method: GET
    content-type: application/json
    url : /post/list/?
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
        status : 200, success: true
        status : 300, success: true
    }
"""


@post.route("/list/", methods=["GET"])
def post_list():
    try:
        parameter_dic = request.args.to_dict()
        if len(parameter_dic) == 0:
            return jsonify({"success": False, "message": "Please input page params"})
        if "page" not in request.args:
            page = 1
        else:
            page = int(request.args["page"])
        if "filter" not in request.args:
            filter = "date"
        else:
            filter = request.args["filter"]
        if filter not in ["date", "notice", "comment", "like"]:
            return jsonify({"success": False, "message": "필터 조건이 잘못되었습니다."})
        if filter == "comment" or filter == "like":
            filter = "num_" + filter
        data = Post.Post.objects().order_by("notice", "-" + filter)[(page - 1) * 10 : page * 10]
        return jsonify({"success": True, "message": json.loads(data.to_json())})
    except:
        return jsonify({"success": False, "message": str(sys.exc_info()[0])})


"""
    게시물 상세 조회 API
    method: GET
    content-type: application/json
    url : /post/?
    header: {
        token : 유저 정보 토큰
    }
    request : {

    }
    parameter : {
        id: string
    }
    response : {
        status : 200, success: true
        status : 300, success: true
    }
"""


@post.route("/", methods=["GET"])
def get_post_detail():
    try:
        parameter_dic = request.args.to_dict()
        if "id" not in request.args:
            return jsonify({"success": False, "message": "Please input id params"})
        id = request.args["id"]
        data = Post.Post.objects(id=id)
        return jsonify({"success": True, "message": json.loads(data.to_json())[0]})
    except:
        return jsonify({"success": False, "message": str(sys.exc_info()[0])})


"""
    게시물 삭제 API
    method: DELETE
    content-type: application/json
    url : /post/?
    header: {
        token : 유저 정보 토큰
    }
    request : {

    }
    parameter : {
        id: string
    }
    response : {
        status : 200, success: true
        status : 300, success: true
    }
"""


@post.route("/", methods=["DELETE"])
def delete_post_detail():
    try:
        decoded = jwt.decode(request.headers["Token"], token_key, algorithms="HS256")
        if "id" not in request.args:
            return jsonify({"success": False, "message": "please input id params"})
        id = request.args["id"]
        Post.Post.objects(id=id, writer=decoded["user_id"]).delete()
        return jsonify({"success": True})
    except:
        return jsonify({"success": False, "message": str(sys.exc_info()[0])})


"""
    게시물 수정 API
    method: PUT
    content-type: application/json
    url : /post/?
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
        status : 200, success: true
        status : 300, success: true
    }
"""


@post.route("/", methods=["PUT"])
def update_post_detail():
    try:
        decoded = jwt.decode(request.headers["Token"], token_key, algorithms="HS256")
        if "id" not in request.args:
            return jsonify({"success": False, "message": "please input id params"})
        id = request.args["id"]
        user_id = decoded["user_id"]
        data = request.json
        Post.Post.objects(id=id, writer=user_id).update(title=data["title"], content=data["content"], tag=data["tag"], notice=data["notice"])
        return jsonify({"success": True})
    except:
        return jsonify({"success": False, "message": str(sys.exc_info()[0])})
