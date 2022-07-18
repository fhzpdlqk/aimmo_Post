import factory
from factory.mongoengine import MongoEngineFactory
from factory import fuzzy
from tests.factory.board_factory import BoardFactory
from app.models import Post
import datetime


class PostFactory(MongoEngineFactory):
    class Meta:
        model = Post

    writer = fuzzy.FuzzyText("writer_")
    date = factory.LazyFunction(datetime.datetime.utcnow)
    title = fuzzy.FuzzyText(prefix="post_title_")
    content = fuzzy.FuzzyText(prefix="post_content_")
    tag = factory.LazyAttribute(lambda n: ["sample_post_tag_1", "sample_post_tag_2"])
    notice = factory.LazyAttribute(lambda n: False)
    like = factory.LazyAttribute(lambda n: [])
    num_comment = factory.LazyAttribute(lambda n: 0)
    board = factory.SubFactory(BoardFactory)
