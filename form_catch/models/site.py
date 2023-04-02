"""Setup the Site model."""
import ormar

from form_catch.database.db import database, metadata


class Site(ormar.Model):
    """Site model definition."""

    class Meta:
        """Define the table name and database to use."""

        tablename = "sites"
        metadata = metadata
        database = database

    id: int = ormar.Integer(primary_key=True)  # type: ignore
    name: str = ormar.String(max_length=100)  # type: ignore
    slug: str = ormar.String(max_length=20, unique=True)  # type: ignore
    email: str = ormar.String(max_length=100)  # type: ignore
