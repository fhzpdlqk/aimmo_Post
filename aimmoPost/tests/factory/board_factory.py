from factory.mongoengine import MongoEngineFactory
from app.models import Board


class BoardFactory(MongoEngineFactory):
    class Meta:
        model = Board

    board_name = "test_board_name"
