---------------
 파이썬 주요 문법 - decorator
---------------

1.정의
^^^^^^^^^^^^^^
다른 함수를 받아 내부를 고치지 않고 추가 기능을 제공할 수 있는 파이썬 문법

2.예시
^^^^^^^^^^^^^^
.. code-block:: python

    from functools import wraps

    def decorate(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            #추가기능 코드 작성
            print("decorator_test")
            return f(*args, **kwargs)
        return decorated_function

    @decorate
    def test_function():
        print("test_function")

    test_function()

test_function 함수를 실행하기전 decorated_function을 통해 추가 기능이 실행된 후test_function이 실행된다

.. code-block:: python

    class decorate(object):
        def __init__(self, param=None):
            self.param = param
        def __call__(self, func):
            @wraps(func)
            def decorated_function(*args, **kwargs):
                #추가기능 작성
                print(summary)
                return func(*args, **kwargs)
    @decorate(param="test_param)
    def test_function():
        print("test_function")

    test_function()

위와 같이 class 형태로 정의하면서 파라미터를 넣어 실행시킬수 있다.
