"""Setup the Site model."""
from sqlalchemy import Column, ForeignKey, Integer, String, Table

from database.db import metadata

Site = Table(
    "sites",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("user_id", Integer, ForeignKey("users.id"), nullable=False),
    Column("name", String(100)),
    Column("slug", String(20), unique=True),
    Column("email", String(100)),
    Column("redirect_url", String(100), nullable=True, default=None),
)
