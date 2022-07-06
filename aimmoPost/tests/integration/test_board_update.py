import pytest
import json
import uuid


@pytest.fixture
def new_data():
    return {"board_name": "test_board_update_name"}


def test_board_update_success(app, board, new_data):
    resp = app.put("/board/" + str(board.id), data=json.dumps(new_data), content_type="application/json")
    data = json.loads(resp.data.decode("utf-8"))
    assert resp.status_code == 200
    assert data == {"success": True}
    board.reload()
    assert board.board_name == "test_board_update_name"


def test_board_update_wrong_boardid(app, board, new_data):
    resp = app.put("/board/" + str(board.id) + "a", data=json.dumps(new_data), content_type="application/json")
    data = json.loads(resp.data.decode("utf-8"))
    assert resp.status_code == 404
    assert not data["success"]
