---------------
 파이썬 주요 문법 - marshmellow
---------------

1. 정의
^^^^^^^^^^^^^^^^^^
data type을 python data type으로 혹은 반대로 바꿔주는 라이브러리

2. 이용법
^^^^^^^^^^^^^^^^
schema 정의

.. code-block:: python

    from marshmallow import fields, Schema, post_load


    class Test:
        def __init__(self, test_string):
            self.test_string = test_string

    class TestSchema(Schema):
        test_string = fields.Str()

        @post_load
        def postload(self, data, **kwargs):
            # load 함수 이후 실행시킬 작업
            # load의 결과를 반환한다.
            # 정의되어 있지 않다면 Schema의 내용이 dictionary형태로 반환된다.
            return Test(**data) #내용이 들어간 객체형태로 반환할 수 있다.



    #dump 예시 > schema에 정의된 내용을 dic형태로 반환
    test = Test("test_string_sample")
    result = TestSchema.dump(test)

    #load 예시 > dic 형태를 TestSchema에 담아 postload 결과값으로 반환
    test = {'test_string': 'test_string_sample'}
    result = TestSchema.load(test)