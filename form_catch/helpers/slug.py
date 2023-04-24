"""Slug helper functions."""
import secrets
import string

from form_catch.database.db import database
from form_catch.models.site import Site


def create_slug(length: int = 8) -> str:
    """Create a random key of a given length."""
    return "".join(
        [
            secrets.choice(string.ascii_letters + string.digits)
            for _ in range(length)
        ]
    )


async def get_site_by_slug(slug: str):
    """Get a site by its slug."""
    return await database.fetch_one(Site.select().where(Site.c.slug == slug))
