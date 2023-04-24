"""Setup the Site model."""
from sqlalchemy import Column, Integer, String, Table

from form_catch.database.db import metadata

Site = Table(
    "sites",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("name", String(100)),
    Column("slug", String(20), unique=True),
    Column("email", String(100)),
    Column("redirect_url", String(100), nullable=True, default=None),
)
