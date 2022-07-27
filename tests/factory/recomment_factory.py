import factory
from factory.mongoengine import MongoEngineFactory
from factory import fuzzy
from app.models import ReComment
from tests.factory.comment_factory import CommentFactory
import datetime


class ReCommentFactory(MongoEngineFactory):
    class Meta:
        model = ReComment

    writer = fuzzy.FuzzyText(prefix="writer_")
    date = factory.LazyFunction(datetime.datetime.utcnow)
    content = fuzzy.FuzzyText(prefix="recomment_content_")
    like = factory.LazyAttribute(lambda n: [])
    comment = factory.SubFactory(CommentFactory)
    is_deleted = factory.LazyAttribute(lambda n: False)
