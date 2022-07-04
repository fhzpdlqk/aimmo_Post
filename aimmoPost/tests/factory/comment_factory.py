import factory
from factory.mongoengine import MongoEngineFactory
from aimmoPost.aimmoPost.models.Comment import Comment
import datetime


class CommentFactory(MongoEngineFactory):
    class Meta:
        model = Comment

    writer = "testid"
    date = factory.LazyFunction(datetime.datetime.utcnow)
    content = "samplecontent_comment"
    re_comment = factory.LazyAttribute(lambda n: [])
    like = factory.LazyAttribute(lambda n: [])
