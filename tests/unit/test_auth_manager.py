"""Unit tests for auth manager.""" ""
from datetime import datetime, timedelta
from unittest.mock import AsyncMock, MagicMock

import jwt
import pytest
from fastapi import HTTPException, status

from managers.auth import AuthManager, ResponseMessages


@pytest.fixture
def mock_user():
    """Create a mock user."""
    return {"id": 1, "banned": False}


@pytest.fixture
def mock_settings():
    """Create a mock settings object."""
    return MagicMock(secret_key="test_secret_key")  # nosec


def test_encode_token(mock_user, mock_settings, mocker):
    """Test that a token is generated with the correct payload."""
    mocker.patch(
        "managers.auth.get_settings",
        return_value=mock_settings,
    )
    token = AuthManager.encode_token(mock_user)
    decoded_token = jwt.decode(
        token, mock_settings.secret_key, algorithms=["HS256"]
    )
    print(datetime.utcnow() + timedelta(minutes=120))
    print(decoded_token["exp"])

    assert decoded_token["sub"] == mock_user["id"]
    assert decoded_token["exp"] == datetime.utcnow() + timedelta(minutes=120)


def test_encode_refresh_token(mock_user, mock_settings):
    """Test that a refresh token is generated with the correct payload."""
    token = AuthManager.encode_refresh_token(mock_user)
    decoded_token = jwt.decode(
        token, mock_settings.secret_key, algorithms=["HS256"]
    )
    assert decoded_token["sub"] == mock_user["id"]
    assert decoded_token["exp"] == datetime.utcnow() + timedelta(
        minutes=60 * 24 * 30
    )


def test_encode_verify_token(mock_user, mock_settings):
    """Test that a verify token is generated with the correct payload."""
    token = AuthManager.encode_verify_token(mock_user)
    decoded_token = jwt.decode(
        token, mock_settings.secret_key, algorithms=["HS256"]
    )
    assert decoded_token["sub"] == mock_user["id"]
    assert decoded_token["typ"] == "verify"
    assert decoded_token["exp"] == datetime.utcnow() + timedelta(minutes=10)


@pytest.mark.asyncio
async def test_refresh(mock_user, mock_settings, mocker):
    """Test that a refresh token is generated with the correct payload."""
    mock_database = AsyncMock()
    mock_database.fetch_one.return_value = mock_user
    mocker.patch("managers.auth.jwt.decode", return_value={"sub": 1})
    mocker.patch(
        "managers.auth.datetime",
        MagicMock(utcnow=MagicMock(return_value=datetime(2023, 1, 1))),
    )
    refresh_token = MagicMock(refresh="test_refresh_token")
    token = await AuthManager.refresh(refresh_token, mock_database)
    decoded_token = jwt.decode(
        token, mock_settings.secret_key, algorithms=["HS256"]
    )
    assert decoded_token["sub"] == mock_user["id"]
    assert decoded_token["exp"] == datetime(2023, 1, 31)


@pytest.mark.asyncio
async def test_refresh_invalid_token(mocker):
    """Test that an invalid refresh token raises an HTTPException."""
    mock_database = MagicMock()
    mocker.patch(
        "managers.auth.jwt.decode", side_effect=jwt.exceptions.InvalidTokenError
    )
    refresh_token = MagicMock(refresh="test_refresh_token")
    with pytest.raises(HTTPException) as exc:
        await AuthManager.refresh(refresh_token, mock_database)
    assert exc.value.status_code == status.HTTP_401_UNAUTHORIZED
    assert exc.value.detail == ResponseMessages.INVALID_TOKEN


@pytest.mark.asyncio
async def test_refresh_expired_token(mocker):
    """Test that an expired refresh token raises an HTTPException."""
    mock_database = MagicMock()
    mocker.patch(
        "managers.auth.jwt.decode",
        side_effect=jwt.exceptions.ExpiredSignatureError,
    )
    refresh_token = MagicMock(refresh="test_refresh_token")
    with pytest.raises(HTTPException) as exc:
        await AuthManager.refresh(refresh_token, mock_database)
    assert exc.value.status_code == status.HTTP_401_UNAUTHORIZED
    assert exc.value.detail == ResponseMessages.EXPIRED_TOKEN
