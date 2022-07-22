---------------
 파이썬 주요 문법 - flask-classful
---------------

1. 정의
^^^^^^^^^^^^^^^^^^
class 기반으로 flask를 구현할 수 있도록 하는 라이브러리

2. 이용법
^^^^^^^^^^^^^^^^^
.. code-block:: python
    from flask_classful import FlaskView, route
    from flask import Flask

    class TestView(FlaskView):
        #route decorator를 활용하여 uri와 method를 정의해준다.
        @route("/", methods=["GET"])
        def get(self):
            # api결과와 status code를 반환해준다
            return "test response", 200

    app = Flask(__name__, static_url_path = '/static')
    #flask app에 view를 등록
    #trailing_slash는 endpoint 마지막 /로 인한 redirect를 막아준다.
    #route_base는 해당 view의 기본 endpoint를 지정
    TestView.register(app, route_base="/test", trailing_slash=False)