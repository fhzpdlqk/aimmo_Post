import factory
from factory.mongoengine import MongoEngineFactory
from aimmoPost.aimmoPost.models.Comment import Comment
from .post_factory import PostFactory
import datetime


class CommentFactory(MongoEngineFactory):
    class Meta:
        model = Comment

    writer = "testid"
    date = factory.LazyFunction(datetime.datetime.utcnow)
    content = "samplecontent_comment"
    like = factory.LazyAttribute(lambda n: [])
    post = PostFactory.create()
