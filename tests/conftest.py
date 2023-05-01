"""Fixtures and configuration for the test suite."""
import pytest
from fastapi.testclient import TestClient

from main import app


@pytest.fixture(scope="module")
def test_app():
    """Fixture to yield a test client for the app."""
    client = TestClient(app)
    yield client
