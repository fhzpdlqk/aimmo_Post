import factory
from factory.mongoengine import MongoEngineFactory
from factory import fuzzy
from tests.factory.board_factory import BoardFactory
from tests.factory.user_factory import UserFactory
from app.models import Post
import datetime
import random


class PostFactory(MongoEngineFactory):
    class Meta:
        model = Post

    writer = factory.SubFactory(UserFactory)
    date = factory.LazyFunction(datetime.datetime.utcnow)
    title = fuzzy.FuzzyText(prefix="post_title_")
    content = fuzzy.FuzzyText(prefix="post_content_")
    tag = factory.LazyAttribute(lambda n: ["sample_post_tag_1", "sample_post_tag_2"])
    notice = factory.LazyAttribute(lambda n: False)
    like = factory.LazyAttribute(lambda n: [UserFactory.create() for _ in range(random.randrange(1,10))])
    num_comment = factory.LazyAttribute(lambda n: random.randrange(1,10))
    board = factory.SubFactory(BoardFactory)
    is_deleted = factory.LazyAttribute(lambda n: False)
