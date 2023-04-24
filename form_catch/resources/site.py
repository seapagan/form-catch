"""Handle site related routes."""
from email_validator import EmailNotValidError, validate_email
from fastapi import APIRouter, HTTPException, status

from form_catch.config.settings import get_settings
from form_catch.database.db import database
from form_catch.helpers.slug import create_slug, get_site_by_slug
from form_catch.models.site import Site
from form_catch.schemas.site import SiteList, SiteRequest, SiteResponse

router = APIRouter(prefix="/site", tags=["Site"])

# RequestSite = Site.get_pydantic(exclude={"id", "slug"})


@router.post(
    "/", response_model=SiteResponse, status_code=status.HTTP_201_CREATED
)
async def create_site(site_data: SiteRequest):
    """Create a new site."""
    slug = create_slug()
    while await get_site_by_slug(slug):
        slug = create_slug()

    try:
        validate_email(site_data.email, check_deliverability=True)
    except EmailNotValidError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(e)
        )

    await database.execute(Site.insert().values(**site_data.dict(), slug=slug))
    return SiteResponse(
        name=site_data.name,
        slug=slug,
        action=f"{get_settings().base_url}/form/{slug}",
    )


@router.get("/{slug}")
async def get_site(slug: str):
    """Get a site by its slug."""
    site = await get_site_by_slug(slug)
    if not site:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Site not found"
        )
    return site


@router.get("/", response_model=list[SiteList])
async def get_sites():
    """Get all sites."""
    return await database.fetch_all(Site.select())


@router.delete("/{slug}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_site(slug: str):  # type: ignore
    """Delete a site by its slug."""
    site = await get_site_by_slug(slug)
    if not site:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Site not found"
        )
    await database.execute(Site.delete().where(Site.c.slug == slug))
