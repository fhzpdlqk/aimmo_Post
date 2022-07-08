import factory
from factory.mongoengine import MongoEngineFactory
from .board_factory import BoardFactory
from aimmoPost.app.schemas.PostSchema import Post
from .board_factory import BoardFactory
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
    like = factory.LazyAttribute(lambda n: [])
    board = BoardFactory.create()
    num_comment = 0
