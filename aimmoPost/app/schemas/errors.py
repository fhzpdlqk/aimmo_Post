from marshmallow import Schema, fields

class ApiErrorSchema(Schema):
    status_code = fields.Integer(data_key="code", required=True)
    message = fields.String()
