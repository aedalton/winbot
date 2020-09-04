import os
import tempfile

import pytest

from winbot import AppFactory


@pytest.fixture
def client_fixture():
    with winbot.AppFactory.create() as client:
        with client.app_context():
            import pdb; pdb.set_trace()
        yield client

def test_client(client_fixture):
    print("entering")
    client_fixture.get('/health')
    print("okay")
    
