"""Define the User model."""
from typing import Annotated

from fastapi import Depends

from form_catch.auth import oauth2_scheme
from form_catch.schemas.user import User


def fake_decode_token(token):
    return User(
        username=token + "fakedecoded",
        email="john@example.com",
        full_name="John Doe",
    )


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    user = fake_decode_token(token)
    return user
