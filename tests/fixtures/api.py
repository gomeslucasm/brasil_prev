from fastapi.testclient import TestClient
import pytest
from api.main import app


@pytest.fixture
def api_client():
    return TestClient(app)
