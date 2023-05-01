"""Handle site related routes."""
from email_validator import EmailNotValidError, validate_email
from fastapi import APIRouter, Depends, HTTPException, Request, status

from config.settings import get_settings
from database.db import database
from helpers.slug import create_slug, get_site_by_slug
from managers.auth import oauth2_schema
from models.enums import RoleType
from models.site import Site
from schemas.site import SiteList, SiteRequest, SiteResponse

router = APIRouter(
    prefix="/site", tags=["Site"], dependencies=[Depends(oauth2_schema)]
)


@router.post(
    "/", response_model=SiteResponse, status_code=status.HTTP_201_CREATED
)
async def create_site(site_data: SiteRequest, request: Request):
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

    await database.execute(
        Site.insert().values(
            **site_data.dict(), slug=slug, user_id=request.state.user.id
        )
    )
    return SiteResponse(
        name=site_data.name,
        slug=slug,
        action=f"{get_settings().base_url}/form/{slug}",
        redirect_url=site_data.redirect_url,
    )


@router.get("/{slug}")
async def get_site(slug: str, request: Request):
    """Get a site by its slug."""
    site = await get_site_by_slug(slug)
    if not site:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Site not found"
        )
    if (
        site["user_id"] != request.state.user.id
        and request.state.user["role"] != RoleType.admin
    ):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not authorized to view this site",
        )

    return SiteResponse(
        name=site["name"],
        slug=site["slug"],
        redirect_url=site["redirect_url"],
        action=f"{get_settings().base_url}/form/{slug}",
    )


@router.get("/", response_model=list[SiteList])
async def get_sites(request: Request):
    """Get all sites."""
    if request.state.user["role"] == RoleType.admin:
        return await database.fetch_all(Site.select())
    else:
        return await database.fetch_all(
            Site.select().where(Site.c.user_id == request.state.user.id)
        )


@router.delete("/{slug}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_site(slug: str, request: Request):  # type: ignore
    """Delete a site by its slug."""
    site = await get_site_by_slug(slug)
    if not site:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Site not found"
        )

    if (
        site["user_id"] != request.state.user.id
        and request.state.user["role"] != RoleType.admin
    ):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not authorized to delete this site",
        )

    await database.execute(Site.delete().where(Site.c.slug == slug))
