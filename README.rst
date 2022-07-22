===========================
AIMMO 신입사원 On-Boarding 과제
===========================

1. 기능
----------------
1. 사용자
~~~~~~~~~~~~~~~
1. 회원가입
2. 로그인
3. 비밀번호 변경

2. 게시판
~~~~~~~~~~~~~~
1. 게시판 목록 조회
2. 게시판 생성
3. 게시판 이름 수정
4. 게시판 삭제

3. 게시글
~~~~~~~~~~~~~~~
1. 게시글 작성
2. 게시글 수정
3. 게시글 목록 조회
4. 게시글 상세 조회
5. 게시글 삭제
6. 게시글 검색
7. 게시글 좋아요 및 좋아요 취소

4. 댓글
~~~~~~~~~~~~~~
1. 댓글 작성
2. 댓글 수정
3. 댓글 삭제
4. 댓글 좋아요 및 좋아요 취소

5. 대댓글
~~~~~~~~~~~~~~
1. 대댓글 작성
2. 대댓글 수정
3. 대댓글 삭제
4. 대댓글 좋아요 및 좋아요 취소

6. 메인페이지
~~~~~~~~~~~~~
1. 최신 게시물 10개 조회
2. 댓글 많은 순 게시물 10개 조회
3. 좋아요 많은 순 게시물 10개 조회

7. 마이페이지
~~~~~~~~~~~~~
1. 내가 쓴 게시물
2. 내가 쓴 댓글
3. 내가 좋아요 한 게시물

2. 사용 기술
-----------------------
 - flask: python 기반의 마이크로 웹 서버 프레임워크
 - flask-classful: class 기반으로 flask를 구현할 수 있도록 하는 라이브러리
 - flask-apispec: flask에서 rest api를 빌드 할 수 있도록 하는 라이브러리
 - mongoengine: python mongodb 드라이버
 - marshmallow: datatype을 python datatype으로 혹은 반대로 바꿔주는 라이브러리

3. 패키지매니저
----------------------
 - poetry

4. API 명세
---------------------
https://aimmopost.azurewebsites.net/api-docs/

5. 주요 내용
---------------------
1. `decorator <./readme/decorator.rst>`_
2. `marshmallow <./readme/marshmallow.rst>`_
3. `flask_classful <./readme/marshmallow.rst>`_
4. `flask_apispec <./readme/flask_apispec.rst>`_
5. `swagger <./readme/swagger.rst>`_

6. 명령어
-------------------------------------------
배포를 위한 requirements.txt 만들기

.. code-block:: console

    poetry export --without-hashes --format=requirements.txt > requirements.txt

poetry 설치

.. code-block:: console

    curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python

app 실행

.. code-block:: console

    poetry run flask run

unit test 실행

.. code-block:: console

    poetry run pytest

