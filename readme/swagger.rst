---------------
 파이썬 주요 문법 - swagger
---------------

1. 정의
^^^^^^^^^^^^^^^^^^
프로젝트에서 정의한 api를 쉽게 확인할 수 있도록 도와준다.

flask에서는 flask-apispec과 apispec 라이브러리를 활용하여 swagger로 보여주기위한 json형태를 제작하고

flask-swagger-ui 라이브러리를 통해 해당 json을 프론트에 보여줄 수 있도록 한다.

2. 이용법
^^^^^^^^^^^^^^^^
먼저 각 api 함수에 flask-apispec을 활용하여 use_kwargs와 marshal_with, doc데코레이션을 달아준다.
이후 annotation을 swagger가 인식할 수 있는 형태로 변경 시키기 위해서 기존 converter를 상속하여 converter를 만들어 준다.

.. code-block:: python

    #새로운 blueprint를 만들어준다.
    api = Blueprint("api", __name__)

    #flask_classful로 정의된 view들을 해당 blueprint에 추가해준다.
    UserView.register(api, route_base="/users", trailing_slash=False)

    #swagger에 사용될 내용을 json형태로 배포한다.
    @bp.route("/apispec")
    def apispec():
        return jsonify(generate_api_spec(title="Aimmo On-Boarding 게시판 만들기",
            version="v1", bp_name=bp.name if isinstance(bp, Blueprint) else None))


.. code-block:: python

    # apispec을 dic형태로 만들어 반환하는 함수이다.
    # 해당 apispec을 만들고 해당 app의 endpoint들과 view_function을 apispec에 path 함수를 이용하여 등록한다.
    def generate_api_spec(title=None, version=None, bp_name=None, global_params=None) -> dict:
        from flask_apispec.paths import rule_to_path

        spec = APISpec(
            title=title,
            version=version,
            openapi_version="3.0.0",
            plugins=(MarshmallowPlugin(),),
        )

        converter = ApiDocConverter(current_app, spec)

        for endpoint, view_func in current_app.view_functions.items():
            endpoint_bp_name = _get_bp_name(endpoint)
            if endpoint_bp_name != bp_name:
                continue
            if hasattr(view_func, "__apispec__"):
                # noinspection PyProtectedMember
                rule = current_app.url_map._rules_by_endpoint[endpoint][0]
                spec.path(
                    view=view_func,
                    path=rule_to_path(rule),
                    operations={method.lower(): converter.get_operation(rule, view_func, converter.get_parent(view_func)) for method in rule.methods if method not in ["OPTIONS", "HEAD"]},
                    parameters=global_params,
                )
        return spec.to_dict()

.. code-block:: python

    #기존 apispec의 converter를 바탕으로 재정의 해준다.
    #아마도 버전이 달라서 저장되는 dic형태가 swagger에서 인식할 수 없도록 되어 있다.
    #따라서 converter의 함수를 활용하고 필요한 부분을 재정의해서 파싱하여 dic형태를 다시 만들어주었다.
    class ApiDocConverter(Converter):
        #최종적으로 모든 dic을 합쳐서 반환하는 함수이다.
        def get_operation(self, rule, view, parent=None):
            from flask_apispec.utils import resolve_annotations, merge_recursive

            annotation = resolve_annotations(view, "docs", parent)
            docs = merge_recursive(annotation.options)
            operation = {
                "responses": self.get_responses(view, parent),
                "parameters": self.get_parameters(rule, view, docs, parent),
            }
            request_body = self.get_request_body(view, parent)
            if request_body:
                operation["requestBody"] = request_body
            docs.pop("params", None)
            return merge_recursive([operation, docs])

자세한 것은 `apidocs_utils.py <../app/apidocs_utils.py>`_ 를 참고하세요.