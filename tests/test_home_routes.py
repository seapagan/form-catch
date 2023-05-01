"""Test the home resource routes."""


def test_root_json(test_app):
    """Test the root route returns a JSON response."""
    response = test_app.get("/")
    assert response.status_code == 200
    print(response.json().keys())
    assert list(response.json().keys()) == ["info", "repository"]
