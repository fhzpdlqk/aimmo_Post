from factory.mongoengine import MongoEngineFactory
from app.models import Board
from factory import fuzzy


class BoardFactory(MongoEngineFactory):
    class Meta:
        model = Board

    board_name = fuzzy.FuzzyText(prefix="board_", length=10)
