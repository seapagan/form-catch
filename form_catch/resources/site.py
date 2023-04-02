"""Handle site related routes."""
from fastapi import APIRouter

from form_catch.helpers.slug import create_slug, get_site_by_slug
from form_catch.models.site import Site

router = APIRouter(prefix="/site", tags=["Site"])

RequestSite = Site.get_pydantic(exclude={"id", "slug"})


@router.post("/", response_model=Site)
async def create_site(site_data: RequestSite):  # type: ignore
    """Create a new site."""
    slug = create_slug()
    while await get_site_by_slug(slug):
        slug = create_slug()

    return await Site(**site_data.dict(), slug=slug).save()
