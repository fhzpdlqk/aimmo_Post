from marshmallow import fields, Schema, post_load
from marshmallow_enum import EnumField
from enum import Enum

class MainPageEnumClass(Enum):
    date = 1
    comment = 2
    like = 3

class MainPageOrderbySchema(Schema):
    orderby = EnumField(MainPageEnumClass)

    @post_load
    def list_info(self, data, **kwargs):
        return {'orderby': data['orderby']}