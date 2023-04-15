"""Set up the User model."""
import ormar

from form_catch.database.db import database, metadata


class User(ormar.Model):
    """User model definition."""

    class Meta:
        """Define the table name and database to use."""

        tablename = "users"
        metadata = metadata
        database = database

    id: int = ormar.Integer(primary_key=True)  # type: ignore
    email: str = ormar.String(max_length=100, unique=True)  # type: ignore
    hashed_password: str = ormar.String(max_length=100)  # type: ignore
    is_active: bool = ormar.Boolean(default=True)  # type: ignore
    is_superuser: bool = ormar.Boolean(default=False)  # type: ignore
