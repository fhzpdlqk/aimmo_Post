from flask_classful import FlaskView, route
from flask_apispec import use_kwargs, marshal_with, doc
from app.schemas.PostSchema import PostListSchema
from app.schemas.MainpageSchema import MainPageOrderbySchema
from app.decorator import login_required
from app.models import Post

class MainPageView(FlaskView):
    decorators = (doc(tags=["Mainpage"]),)
    @route("/", methods=["GET"])
    @doc(summary="메인페이지 게시물", description="메인페이지 게시물")
    @login_required
    @use_kwargs(MainPageOrderbySchema, location='query')
    @marshal_with(PostListSchema(many=True), code=200, description="게시물 최신, 댓글, 좋아요순 10개")
    def recent_post(self, orderby):
        post_list = Post.objects(is_deleted=False).order_by(f"-{orderby}")[:10]
        return post_list, 200

