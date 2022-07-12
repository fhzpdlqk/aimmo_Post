from json import dumps
import pytest

class Test_MainPageView:
    class Test_Recent_List:
        @pytest.fixture
        def trans_api(self, client):
            return client.get('/mainpage/recent', content_type="application/json")

        def test_상태코드_200(self,trans_api):
            assert trans_api.status_code == 200

        def test_목록_최신순_여부(self, trans_api):
            post_list = trans_api.json["message"]
            for index in range(1,len(post_list)):
                assert post_list[index-1]["date"] >= post_list[index]["date"]


    class Test_Comment_List:
        @pytest.fixture
        def trans_api(self, client):
            return client.get('/mainpage/comment', content_type="application/json")

        def test_상태코드_200(self,trans_api):
            assert trans_api.status_code == 200

        def test_목록_최신순_여부(self, trans_api):
            post_list = trans_api.json["message"]
            for index in range(1,len(post_list)):
                assert post_list[index-1]["num_comment"] >= post_list[index]["num_comment"]

    class Test_like_List:
        @pytest.fixture
        def trans_api(self, client):
            return client.get('/mainpage/like', content_type="application/json")

        def test_상태코드_200(self,trans_api):
            assert trans_api.status_code == 200

        def test_목록_최신순_여부(self, trans_api):
            post_list = trans_api.json["message"]
            for index in range(1,len(post_list)):
                assert post_list[index-1]["num_like"] >= post_list[index]["num_like"]
