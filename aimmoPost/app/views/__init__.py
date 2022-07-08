from flask_restx import Api,Resource,reqparse

from app.views.user import UserView
from app.views.comment import CommentView
from app.views.mypage import MyPageView
from app.views.post import PostView
from app.views.recomment import ReCommentView
from app.views.board import BoardView
from app.views.mainpage import MainPageView

def register_api(app):
    UserView.register(app, route_base="/users")
    BoardView.register(app, route_base="/boards")
    PostView.register(app, route_base="/boards/<string:board_id>/posts")
    CommentView.register(app, route_base="/boards/<string:board_id>/posts/<string:post_id>/comments")
    ReCommentView.register(app, route_base="/boards/<string:board_id>/posts/<string:post_id>/comments/<string:comment_id>/recomments")
    MainPageView.register(app, route_base="/mainpage")
    MyPageView.register(app, route_base="/mypage")
