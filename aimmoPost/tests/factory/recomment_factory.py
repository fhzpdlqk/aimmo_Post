import factory
from factory.mongoengine import MongoEngineFactory
from app.models import ReComment
from tests.factory.comment_factory import CommentFactory
import datetime


class ReCommentFactory(MongoEngineFactory):
    class Meta:
        model = ReComment

    writer = "testid"
    date = factory.LazyFunction(datetime.datetime.utcnow)
    content = "samplecontent_comment"
    like = factory.LazyAttribute(lambda n: [])
    comment = factory.SubFactory(CommentFactory)
