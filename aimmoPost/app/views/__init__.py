from app.views.user import UserView
from app.views.comment import CommentView
from app.views.mypage import MyPageView
from app.views.post import PostView
from app.views.recomment import ReCommentView
from app.views.board import BoardView
from app.views.mainpage import MainPageView
from flask_swagger_ui import get_swaggerui_blueprint
from flask_classful_apispec import APISpec
import json


def register_api(app):
    UserView.register(app, route_base="/users", trailing_slash=False)
    BoardView.register(app, route_base="/boards", trailing_slash=False)
    PostView.register(app, route_base="/boards/<string:board_id>/posts", trailing_slash=False)
    CommentView.register(app, route_base="/boards/<string:board_id>/posts/<string:post_id>/comments", trailing_slash=False)
    ReCommentView.register(app, route_base="/boards/<string:board_id>/posts/<string:post_id>/comments/<string:comment_id>/recomments", trailing_slash=False)
    MainPageView.register(app, route_base="/mainpage",trailing_slash=False)
    MyPageView.register(app, route_base="/mypage", trailing_slash=False)

    app.config["DOC_TITLE"] = "Swagger petstore"
    app.config["DOC_VERSION"] = "0.1.1"
    app.config["DOC_OPEN_API_VERSION"] = "3.0.2"
    register_swagger(app)


def register_swagger(app):
    spec = APISpec(app)
    with app.test_request_context():
        spec.paths(UserView, app)
        spec.paths(BoardView, app)
        spec.paths(PostView, app)
        spec.paths(CommentView, app)
        spec.paths(ReCommentView, app)
        spec.paths(MyPageView, app)
        spec.paths(MainPageView, app)

        api_key_scheme = {"type": "uuid", "in": "header", "name": "Authorization"}
        board_id_scheme = {"type": "string", "in": "path", "name": "board_id"}
        post_id_scheme = {"type": "string", "in": "path", "name": "post_id"}
        comment_id_scheme = {"type": "string", "in": "path", "name": "comment_id"}
        recomment_id_scheme = {"type": "string", "in": "path", "name": "recomment_id"}
        page_scheme = {"type": "integer", "in": "query", "name": "page"}
        size_scheme = {"type": "integer", "in": "query", "name": "size"}

        spec.components.security_scheme(component_id="Authorization", component=api_key_scheme)
        spec.components.parameter(component_id="board_id", component=board_id_scheme, location='path')
        spec.components.parameter(component_id="post_id", component=post_id_scheme, location='path')
        spec.components.parameter(component_id="comment_id", component=comment_id_scheme, location='path')
        spec.components.parameter(component_id="recomment_id", component=recomment_id_scheme, location='path')
        spec.components.parameter(component_id="page", component=page_scheme, location='query')
        spec.components.parameter(component_id="size", component=size_scheme, location='query')

        with open('./app/static/swagger.json', 'w', encoding='utf-8') as make_file:
            json.dump(spec.to_dict(), make_file, indent="\t", ensure_ascii=False)

    SWAGGER_URL = '/api/docs'  # URL for exposing Swagger UI (without trailing '/')
    API_URL = '/static/swagger.json'  # Our API url (can of course be a local resource)

    # Call factory function to create our blueprint
    swaggerui_blueprint = get_swaggerui_blueprint(
        SWAGGER_URL,  # Swagger UI static files will be mapped to '{SWAGGER_URL}/dist/'
        API_URL,
        config={  # Swagger UI config overrides
            'app_name': "Test application"
        },
        # oauth_config={  # OAuth config. See https://github.com/swagger-api/swagger-ui#oauth2-configuration .
        #    'clientId': "your-client-id",
        #    'clientSecret': "your-client-secret-if-required",
        #    'realm': "your-realms",
        #    'appName': "your-app-name",
        #    'scopeSeparator': " ",
        #    'additionalQueryStringParams': {'test': "hello"}
        # }
    )

    app.register_blueprint(swaggerui_blueprint)
