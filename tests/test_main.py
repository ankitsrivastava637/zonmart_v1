
import pytest
from fastapi.testclient import TestClient
from app.main import app
from sqlalchemy import create_engine
from app.models import User  # Import User model
from app.database.crud import Base
from pytest_mock import mocker


# Import the SQLAlchemy session and engine you use in your app
from app.main import get_db

# Initialize the test client
client = TestClient(app)

# Define test data (you can customize this)
test_user_data = {
    "username": "testname1",
    "password": "testpassword",
    "address" : "testaddress"
}


# Use pytest fixtures to set up and tear down the database
@pytest.fixture(scope="module")
def setup_database():
    # Use an in-memory SQLite database for testing
    db_url = "sqlite:///:memory:"
    engine = create_engine(db_url)
    testing_session = get_db()

    # Create tables in the in-memory database
    Base.metadata.create_all(bind=engine)

    yield testing_session

    # Clean up after the tests
    testing_session.close()
    engine.dispose()

def test_create_user(setup_database, mocker):
    # Test creating a user
    db_mock = mocker.MagicMock()
    mocker.patch('app.main.get_db', return_value=setup_database)

    response = client.post("/create_user/", json=test_user_data)
    assert response.status_code == 200
    user = response.json()
    assert user["username"] == test_user_data["username"]


if __name__ == "__main__":
    pytest.main()
