import factory
from factory.mongoengine import MongoEngineFactory
from aimmoPost.aimmoPost.models.Board import Board
import datetime


class BoardFactory(MongoEngineFactory):
    class Meta:
        model = Board

    board_name = "test_board_name"
    post = factory.LazyAttribute(lambda n: [])
