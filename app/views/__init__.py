from app.views.user import UserView
from app.views.comment import CommentView
from app.views.mypage import MyPageView
from app.views.post import PostView
from app.views.recomment import ReCommentView
from app.views.board import BoardView
from app.views.mainpage import MainPageView
from flask import Blueprint, jsonify
from flask_swagger_ui import get_swaggerui_blueprint
from flask_apispec import marshal_with
from app.errors import ApiError, ApiErrorSchema

api = Blueprint("api", __name__)
def register_api(app):
    UserView.register(api, route_base="/users", trailing_slash=False)
    BoardView.register(api, route_base="/boards", trailing_slash=False)
    PostView.register(api, route_base="/boards/<string:board_id>/posts", trailing_slash=False)
    CommentView.register(api, route_base="/boards/<string:board_id>/posts/<string:post_id>/comments", trailing_slash=False)
    ReCommentView.register(api, route_base="/boards/<string:board_id>/posts/<string:post_id>/comments/<string:comment_id>/recomments", trailing_slash=False)
    MainPageView.register(api, route_base="/",trailing_slash=False)
    MyPageView.register(api, route_base="/mypage", trailing_slash=False)

    register_swagger(api)
    app.register_blueprint(api)
    SWAGGER_URL = '/api-docs'  # URL for exposing Swagger UI (without trailing '/')
    API_URL = '/apispec'  # Our API url (can of course be a local resource)

    # Call factory function to create our blueprint
    swaggerui_blueprint = get_swaggerui_blueprint(
        SWAGGER_URL,  # Swagger UI static files will be mapped to '{SWAGGER_URL}/dist/'
        API_URL,
        config={  # Swagger UI config overrides
            'app_name': "Test application"
        },
    )

    app.register_blueprint(swaggerui_blueprint)
    register_error_handler(app)


def register_swagger(bp):
    from app.apidocs_utils import generate_api_spec

    @bp.route("/apispec")
    def apispec():
        return jsonify(generate_api_spec(title="Aimmo On-Boarding 게시판 만들기", version="v1", bp_name=bp.name if isinstance(bp, Blueprint) else None))

def register_error_handler(bp):
    bp.register_error_handler(ApiError, handle_api_error)

@marshal_with(ApiErrorSchema())
def handle_api_error(e: ApiError):
    return e, e.status_code