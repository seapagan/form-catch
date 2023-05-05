"""Test the authentication routes of the application."""
import pytest

from models.enums import RoleType
from models.user import User

email_fn_to_patch = "managers.user.EmailManager.template_send"
register_path = "/register"


@pytest.mark.asyncio
async def test_register_new_user(test_app, db, mocker):
    """Ensure a new user can register."""
    # disable email sending by mocking the function
    post_body = {
        "email": "testuser@testuser.com",
        "first_name": "Test",
        "last_name": "User",
        "password": "test12345!",
    }
    mock_send = mocker.patch(email_fn_to_patch)
    response = test_app.post(
        register_path,
        json=post_body,
    )

    assert response.status_code == 201
    assert list(response.json().keys()) == ["token", "refresh"]
    assert type(response.json()["token"]) is str
    assert type(response.json()["refresh"]) is str

    users_data = await db.fetch_one(User.select())
    assert users_data["email"] == post_body["email"]
    assert users_data["first_name"] == post_body["first_name"]
    assert users_data["last_name"] == post_body["last_name"]
    assert users_data["password"] != post_body["password"]
    assert users_data["verified"] is False
    assert users_data["role"] == RoleType.user

    mock_send.assert_called_once()


@pytest.mark.asyncio
async def test_register_new_user_with_bad_email(test_app, db, mocker):
    """Ensure an invalid email address fails, and no email is sent."""
    # mock the email sending function
    mock_send = mocker.patch(email_fn_to_patch)

    response = test_app.post(
        register_path,
        json={
            "email": "bad_email",
            "first_name": "Test",
            "last_name": "User",
            "password": "test12345!",
        },
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "This email address is not valid"

    users_data = await db.fetch_all(User.select())
    assert len(users_data) == 0

    mock_send.assert_not_called()


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "post_body",
    [
        {},
        {
            "email": "",
            "first_name": "Test",
            "last_name": "User",
            "password": "test12345!",
        },
        {
            "email": "email@testuser.com",
            "first_name": "",
            "last_name": "User",
            "password": "test12345!",
        },
        {
            "email": "email@testuser.com",
            "first_name": "Test",
            "last_name": "",
            "password": "test12345!",
        },
        {
            "email": "email@testuser.com",
            "first_name": "Test",
            "last_name": "User",
            "password": "",
        },
    ],
)
async def test_register_new_user_with_missing_data(
    test_app, db, mocker, post_body
):
    """Ensure registering with missing data fails, and no email is sent."""
    # mock the email sending function
    mock_send = mocker.patch(email_fn_to_patch)

    response = test_app.post(register_path, json=post_body)

    assert response.status_code == 400 or 422

    users_data = await db.fetch_all(User.select())
    assert len(users_data) == 0

    mock_send.assert_not_called()
