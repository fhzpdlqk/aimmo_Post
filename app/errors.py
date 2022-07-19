class ApiError(Exception):
    status_code = 400

    def __init__(self, message, status_code=None):
        Exception.__init__(self)
        self.message = message
        self.status_code = status_code


from marshmallow import Schema, fields


class ApiErrorSchema(Schema):
    status_code = fields.Integer(data_key="code", required=True)
    message = fields.String()
