import pytest
import mongoengine as me
from flask import current_app

@pytest.fixture
def headers(token):
    return {
        "Authorization": token,
        'Content-Type': 'application/json'
    }
