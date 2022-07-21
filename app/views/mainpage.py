from flask import jsonify
from flask_classful import FlaskView, route
from flask_apispec import use_kwargs, marshal_with, doc
from app.schemas.PostSchema import PostListSchema
from app.schemas.MainpageSchema import MainPageFilterSchema
from app.decorator import login_required
from app.models import Post

class MainPageView(FlaskView):
    decorators = (doc(tags=["Mainpage"]),)
    @route("/", methods=["GET"])
    @doc(summary="최근순 게시물 10개", description="최근순 게시물 10개")
    @login_required
    @use_kwargs(MainPageFilterSchema, location='query')
    @marshal_with(PostListSchema(many=True), code=200, description="게시물 최근목록 10개")
    def recent_post(self, filter):
        post_list = Post.objects(is_deleted=False).order_by(f"-{filter}")[:10]
        return post_list, 200

