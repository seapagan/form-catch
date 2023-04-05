"""Handle site related routes."""
from fastapi import APIRouter, HTTPException, status

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


@router.get("/{slug}", response_model=Site)
async def get_site(slug: str):  # type: ignore
    """Get a site by its slug."""
    site = await get_site_by_slug(slug)
    if not site:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Site not found"
        )
    return site


@router.get("/", response_model=list[Site])
async def get_sites():  # type: ignore
    """Get all sites."""
    return await Site.objects.all()


@router.delete("/{slug}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_site(slug: str):  # type: ignore
    """Delete a site by its slug."""
    site = await get_site_by_slug(slug)
    if not site:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Site not found"
        )
    await site.delete()
