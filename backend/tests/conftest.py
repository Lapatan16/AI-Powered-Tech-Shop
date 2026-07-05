import pytest
from fastapi.testclient import TestClient
from src.api import api

@pytest.fixture(scope="session")
def client():
    with TestClient(api) as c:
        yield c