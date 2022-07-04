import factory
from factory.mongoengine import MongoEngineFactory
from aimmoPost.aimmoPost.models.Post import Post
import datetime


class PostFactory(MongoEngineFactory):
    class Meta:
        model = Post

    writer = "testid"
    date = factory.LazyFunction(datetime.datetime.utcnow)
    title = "sampletitle"
    content = "samplecontent"
    tag = ["tag_1", "tag_2"]
    notice = True
    comment = factory.LazyAttribute(lambda n: [])
    like = factory.LazyAttribute(lambda n: [])
