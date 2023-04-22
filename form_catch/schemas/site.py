from pydantic import BaseModel

""" Define response schema for site data."""


class SiteResponse(BaseModel):
    """Define schema for site data."""

    name: str
    slug: str
    action: str
