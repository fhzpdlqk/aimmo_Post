from marshmallow import fields, Schema, post_load, validate

class MainPageOrderbySchema(Schema):
    orderby = fields.Str(validate=validate.OneOf(["date","comment","like"]))
