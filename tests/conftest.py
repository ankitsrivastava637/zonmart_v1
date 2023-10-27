import pytest
from fastapi.testclient import TestClient
from app.main import app  # Import your FastAPI app instance

# Define a fixture for creating a FastAPI test client
@pytest.fixture
def test_client():
    client = TestClient(app)
    return client
