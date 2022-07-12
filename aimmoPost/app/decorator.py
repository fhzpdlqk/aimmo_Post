from functools import wraps
from flask import g, request, current_app, jsonify
import jwt

from app.models import Board, Post, Comment, ReComment


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not 'Authorization' in request.headers:
            return jsonify(message="로그인하지 않은 사용자입니다."), 401
        try:
            decoded = jwt.decode(request.headers.get('Authorization'), current_app.config["TOKEN_KEY"], current_app.config["ALGORITHM"])
        except jwt.InvalidTokenError:
            return jsonify(message="유효하지 않은 토큰입니다."), 401
        g.is_master = decoded["is_master"]
        g.user_id = decoded["user_id"]
        return f(*args, **kwargs)

    return decorated_function

def master_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if g.is_master is False:
            return jsonify(message="허가되지 않은 사용자입니다."), 403
        return f(*args, **kwargs)
    return decorated_function

def check_board(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        print(kwargs)
        if not Board.objects(id=kwargs["board_id"]):
            return jsonify(message="없는 게시판입니다"), 404
        return f(*args, **kwargs)
    return decorated_function

def check_post(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not Post.objects(id=kwargs["post_id"]):
            return jsonify(message="없는 게시물입니다"), 404
        return f(*args, **kwargs)
    return decorated_function

def check_post_writer(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        post = Post.objects(id=kwargs["post_id"])
        if not post:
            return jsonify(message="없는 게시물입니다"), 404
        elif post.get().writer != g.user_id:
            return jsonify(message="작성자 아이디가 아닙니다."), 401
        return f(*args, **kwargs)
    return decorated_function

def check_comment(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not Comment.objects(id=kwargs["comment_id"]):
            return jsonify(message="없는 댓글입니다"), 404
        return f(*args, **kwargs)
    return decorated_function

def check_comment_writer(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        comment = Comment.objects(id=kwargs["comment_id"])
        if not comment:
            return jsonify(message="없는 댓글입니다"), 404
        elif comment.get().writer != g.user_id:
            return jsonify(message="작성자 아이디가 아닙니다."), 401
        return f(*args, **kwargs)
    return decorated_function

def check_recomment(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not ReComment.objects(id=kwargs["recomment_id"]):
            return jsonify(message="없는 대댓글입니다"), 404
        return f(*args, **kwargs)
    return decorated_function

def check_recomment_writer(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        recomment = ReComment.objects(id=kwargs["recomment_id"])
        if not recomment:
            return jsonify(message="없는 대댓글입니다"), 404
        elif recomment.get().writer != g.user_id:
            return jsonify(message="작성자 아이디가 아닙니다."), 401
        return f(*args, **kwargs)
    return decorated_function