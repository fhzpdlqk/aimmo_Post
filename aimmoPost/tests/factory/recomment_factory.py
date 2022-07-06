import factory
from factory.mongoengine import MongoEngineFactory
from aimmoPost.aimmoPost.models.ReComment import ReComment
from .comment_factory import CommentFactory
import datetime


class ReCommentFactory(MongoEngineFactory):
    class Meta:
        model = ReComment

    writer = "testid"
    date = factory.LazyFunction(datetime.datetime.utcnow)
    content = "samplecontent_comment"
    like = factory.LazyAttribute(lambda n: [])
    comment = CommentFactory.create().id
