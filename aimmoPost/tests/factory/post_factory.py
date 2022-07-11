import factory
from factory.mongoengine import MongoEngineFactory
from .board_factory import BoardFactory
from app.models import Post
import datetime


class PostFactory(MongoEngineFactory):
    class Meta:
        model = Post

    writer = "test_user_id"
    date = factory.LazyFunction(datetime.datetime.utcnow)
    title = "sample_post_title"
    content = "sample_content_title"
    tag = ["sample_post_tag_1", "sample_post_tag_2"]
    notice = True
    like = factory.LazyAttribute(lambda n: [])
    board = factory.SubFactory(BoardFactory)
    num_comment = 0
