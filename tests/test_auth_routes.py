"""Test the authentication routes of the application."""
import pytest

from models.enums import RoleType
from models.user import User


def mock_template_send(self, backgroundtasks, email_data):
    """Mock the template_send method."""
    return None


@pytest.mark.asyncio
async def test_register_new_user(test_app, db, mocker):
    """Ensure a new user can register."""
    # disable email sending
    mocker.patch("managers.user.EmailManager.template_send", mock_template_send)

    post_body = {
        "email": "testuser@testing.com",
        "first_name": "Test",
        "last_name": "User",
        "password": "test12345!",
    }
    response = test_app.post(
        "/register",
        json=post_body,
    )

    users_data = await db.fetch_one(User.select())

    assert response.status_code == 201
    assert len(response.json()) == 2

    assert users_data["email"] == post_body["email"]
    assert users_data["first_name"] == post_body["first_name"]
    assert users_data["last_name"] == post_body["last_name"]
    assert users_data["password"] != post_body["password"]
    assert users_data["verified"] is False
    assert users_data["role"] == RoleType.user


@pytest.mark.asyncio
async def test_register_new_user_bad_email(test_app, db, mocker):
    """Ensure submitted email address is valid when registering."""
    # disable email sending
    mocker.patch("managers.user.EmailManager.template_send", mock_template_send)

    response = test_app.post(
        "/register",
        json={
            "email": "bad_email",
            "first_name": "Test",
            "last_name": "User",
            "password": "test12345!",
        },
    )

    users_data = await db.fetch_all(User.select())
    assert len(users_data) == 0

    assert response.status_code == 400
    assert response.json()["detail"] == "This email address is not valid"
