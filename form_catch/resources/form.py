"""Routes for handling form data."""
from fastapi import APIRouter, Request

router = APIRouter(prefix="/form", tags=["Form Handling"])


@router.get("/{slug}")
@router.post("/{slug}")
async def respond_to_form(slug: str, request: Request):
    """Get the supplied form data and email it.

    Note that the slug is used to determine the email address to send the form
    data to.

    Also, this route responds to both GET and POST requests.
    """
    form_data = await request.form()
    return {
        "message": f"Get form data by slug: {slug}",
        "form_data": form_data,
    }
