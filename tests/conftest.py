"""Fixtures and configuration for the test suite."""
import databases
import pytest
import sqlalchemy
from fastapi.testclient import TestClient

from database.db import metadata
from main import app
from models import site, user  # noqa F401

DATABASE_URL = "sqlite:///./test.db"
database = databases.Database(DATABASE_URL)


# Override the database connection to use the test database.
async def get_database_override():
    """Return the database connection for testing."""
    await database.connect()
    yield database


def pytest_sessionstart(session):
    """Create the test database."""
    engine = sqlalchemy.create_engine(
        DATABASE_URL, connect_args={"check_same_thread": False}
    )
    metadata.create_all(engine)


def pytest_sessionfinish(session):
    """Drop the test database."""
    engine = sqlalchemy.create_engine(
        DATABASE_URL, connect_args={"check_same_thread": False}
    )
    metadata.drop_all(engine)


@pytest.fixture(scope="module")
def test_app():
    """Fixture to yield a test client for the app."""
    client = TestClient(app)
    yield client
