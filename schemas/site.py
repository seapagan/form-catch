"""Define schema for site data."""
from pydantic import BaseModel

""" Define response schema for site data."""


class SiteRequest(BaseModel):
    """Define schema for site data."""

    name: str
    email: str
    redirect_url: str


class SiteResponse(BaseModel):
    """Define schema for site data."""

    name: str
    slug: str
    action: str
    redirect_url: str


class SiteList(SiteRequest):
    """Specifically for listing sites."""

    slug: str
