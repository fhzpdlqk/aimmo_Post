from marshmallow import fields, Schema, post_load, validate

class MainPageOrderbySchema(Schema):
    orderby = fields.Str(validate=validate.OneOf(["date","comment","like"]))

    @post_load
    def list_info(self, data, **kwargs):
        return {'orderby': data['orderby']}