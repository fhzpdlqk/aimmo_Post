---------------
 파이썬 주요 문법 - flask-apispec
---------------

1. 정의
^^^^^^^^^^^^^^^^^^
 - flask에서 rest api를 빌드 할 수 있도록 하는 라이브러리
 - 추가로 swagger를 위한 annotation을 자동으로 추가해준다

2. 이용법
^^^^^^^^^^^^^^^^^
.. code-block:: python

    from flask_apispec import use_kwargs, marshal_with, doc
    from marshmallow import fields, Schema, post_load

    class Test:
        def __init__(self, test_string):
            self.test_string = test_string

    class TestSchema(Schema):
        test_string = fields.Str()
        @post_load
        def postload(self, data, **kwargs):
            return {"test": Test(**data) }

    @route('/', methods=["POST"])
    #api request를 TestSchema로 load시켜준다. 이때 반환값의 key값과 같은 매개변수로 결과를 준다.
    @use_kwargs(TestSchema())
    #api의 return값을 MarshalSchema로 dump시켜 결과를 반환한다.
    @doc(summary="test_summary", description="test_description)
    #swagger에 필요한 summary, description annotation을 추가해준다.
    @marshal_with(MarshalSchema, code=200)
    def post(self, test=None):
        return Marshal(), 200

flask apispec의 각 decoration 함수들은 동작과 동시에 필요한 annotation을 추가해준다.

따라서 swagger를 연동할 때 반드시 필요한 작업이다.

