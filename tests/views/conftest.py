import pytest

@pytest.fixture
def headers(token):
    return {
        "Authorization": token,
        'Content-Type': 'application/json'
    }
