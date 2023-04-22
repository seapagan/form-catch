"""Handle site related routes."""
from email_validator import EmailNotValidError, validate_email
from fastapi import APIRouter, HTTPException, status

from form_catch.config.settings import get_settings
from form_catch.helpers.slug import create_slug, get_site_by_slug
from form_catch.models.site import Site
from form_catch.schemas.site import SiteResponse

router = APIRouter(prefix="/site", tags=["Site"])

RequestSite = Site.get_pydantic(exclude={"id", "slug"})


@router.post(
    "/", response_model=SiteResponse, status_code=status.HTTP_201_CREATED
)
async def create_site(site_data: RequestSite):  # type: ignore
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

    response = await Site(**site_data.dict(), slug=slug).save()
    return SiteResponse(
        name=response.name,
        slug=response.slug,
        action=f"{get_settings().base_url}/form/{slug}",
    )


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
