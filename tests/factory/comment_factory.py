import factory
from factory import fuzzy
from factory.mongoengine import MongoEngineFactory
from app.models import Comment
from .post_factory import PostFactory
import datetime
import random


class CommentFactory(MongoEngineFactory):
    class Meta:
        model = Comment

    writer = fuzzy.FuzzyText(prefix="writer_")
    date = factory.LazyFunction(datetime.datetime.utcnow)
    content = fuzzy.FuzzyText(prefix="comment_content")
    like = factory.LazyAttribute(lambda n: [])
    post = factory.SubFactory(PostFactory)
    is_deleted = factory.LazyAttribute(lambda n: False)
    num_recomment = factory.LazyAttribute(lambda n: random.randrange(1,10))