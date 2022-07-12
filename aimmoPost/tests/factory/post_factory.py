import factory
from factory.mongoengine import MongoEngineFactory
from tests.factory.board_factory import BoardFactory
from app.models import Post
import datetime


class PostFactory(MongoEngineFactory):
    class Meta:
        model = Post

    writer = "test_user_id"
    date = factory.LazyFunction(datetime.datetime.utcnow)
    title = "sample_post_title"
    content = "sample_content_title"
    tag = factory.LazyAttribute(lambda n: ["sample_post_tag_1", "sample_post_tag_2"])
    notice = factory.LazyAttribute(lambda n: False)
    like = factory.LazyAttribute(lambda n: [])
    num_comment = factory.LazyAttribute(lambda n: 0)
    board = factory.SubFactory(BoardFactory)
