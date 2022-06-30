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
    개시물 리스트 조회 API
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
        page = int(request.args["page"])
        data = Post.Post.objects().order_by("date")[(page - 1) * 10 : page * 10]
        return jsonify({"success": True, "message": json.loads(data.to_json())})
    except:
        return jsonify({"success": False, "message": str(sys.exc_info()[0])})