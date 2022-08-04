import pytest
from app.app import app

@pytest.fixture(scope="session")
def client():
    return app.test_client()