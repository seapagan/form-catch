"""Routes for handling form data."""
from fastapi import APIRouter, Request

from form_catch.helpers.slug import get_site_by_slug

router = APIRouter(prefix="/form", tags=["Form Handling"])


@router.get("/{slug}")
@router.post("/{slug}")
async def respond_to_form(slug: str, request: Request):
    """Get the supplied form data and email it.

    Note that the slug is used to determine the email address to send the form
    data to.

    Also, this route responds to both GET and POST requests.
    """
    site = await get_site_by_slug(slug)
    if not site:
        return {"detail": "Site not found."}
    form_data = await request.form()
    return {
        "message": f"Get form data by slug: {slug}",
        "form_data": form_data,
    }
