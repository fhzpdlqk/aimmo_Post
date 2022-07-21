from marshmallow import fields, Schema, post_load
from marshmallow.validate import Length

class MainPageFilterSchema(Schema):
    filter = fields.Str()

    @post_load
    def list_info(self, data, **kwargs):
        if data['filter'] == 'comment' or data['filter'] == 'like':
            return {'filter': data['filter']}
        else:
            return {'filter': 'date'}