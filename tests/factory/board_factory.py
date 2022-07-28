import factory
from factory.mongoengine import MongoEngineFactory
from app.models import Board
from factory import fuzzy


class BoardFactory(MongoEngineFactory):
    class Meta:
        model = Board

    name = fuzzy.FuzzyText(prefix="board_", length=10)
    is_deleted = factory.LazyAttribute(lambda n: False)
