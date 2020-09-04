import os
import json

import pytest

#from winbot.app import AppFactory
from winbot import config
from winbot.app import AppFactory
from winbot.msg_generator import SLACK_CONN


@pytest.fixture
def app_fixture():
    with AppFactory.create().test_client() as client:
        # with flaskr.app.app_context():
        yield client


@pytest.mark.skip()
def test_channel_members():
    response = SLACK_CONN.conversations_members(
        channel=config.SLACK_CHANNEL_ID)
    user_ids = response["members"]
    print(f"user_ids: {user_ids}")
    assert user_ids


def test_client(app_fixture):
    response = app_fixture.get('/health')
    assert "okay" in str(response.data)
