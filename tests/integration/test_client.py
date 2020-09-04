import os
import tempfile

import pytest

from winbot.app import AppFactory


@pytest.fixture
def client_fixture():
    with AppFactory.create() as client:
        with client.app_context():
            response = SLACK_CONN.conversations_members(channel=SLACK_CHANNEL_ID)
            user_ids = response["members"]
            print(f"user_ids: {user_ids}")
            import pdb; pdb.set_trace()
        yield client

def test_client(client_fixture):
    print("entering")
    client_fixture.get('/health')
    print("okay")
    
