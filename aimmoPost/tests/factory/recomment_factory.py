import factory
from factory.mongoengine import MongoEngineFactory
from aimmoPost.aimmoPost.models.Comment import ReComment
import datetime


class ReCommentFactory(MongoEngineFactory):
    class Meta:
        model = ReComment

    writer = "testid"
    date = factory.LazyFunction(datetime.datetime.utcnow)
    content = "samplecontent_comment"
    like = factory.LazyAttribute(lambda n: [])