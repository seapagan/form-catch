"""Define schemas needed for the User model."""
from pydantic import BaseModel


class User(BaseModel):
    """The User model schema."""

    username: str
    email: str | None = None
    full_name: str | None = None
    disabled: bool | None = None
