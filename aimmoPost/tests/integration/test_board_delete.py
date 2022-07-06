import pytest
import json
import uuid


def test_board_delete_success(app, id_token, board):
    token = id_token
    resp = app.delete("/board/" + str(board.id), content_type="application/json", headers={"Token": token})
    data = json.loads(resp.data.decode("utf-8"))
    assert resp.status_code == 200
    assert data == {"success": True}


def test_board_delete_no_postid(app, id_token, board):
    token = id_token
    resp = app.delete("/post/", content_type="application/json", headers={"Token": token})
    assert resp.status_code == 404
