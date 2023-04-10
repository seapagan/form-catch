"""Routes for handling form data."""
from fastapi import APIRouter, BackgroundTasks, HTTPException, Request, status
from fastapi.responses import RedirectResponse
from fastapi_mail import FastMail, MessageSchema, MessageType
from pydantic import EmailStr

from form_catch.helpers.slug import get_site_by_slug

router = APIRouter(prefix="/form", tags=["Form Handling"])


@router.get("/{slug}", status_code=status.HTTP_204_NO_CONTENT)
@router.post("/{slug}", status_code=status.HTTP_204_NO_CONTENT)
async def respond_to_form(
    slug: str, request: Request, backgroundtasks: BackgroundTasks
):
    """Get the supplied form data and email it.

    Note that the slug is used to determine the email address to send the form
    data to.

    Also, this route responds to both GET and POST requests.
    """
    site = await get_site_by_slug(slug)
    if not site:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Site not found."
        )
    method = request.method

    if method == "GET":
        form_data = request.query_params
    elif method == "POST":
        form_data = await request.form()
    else:
        raise HTTPException(
            status_code=status.HTTP_405_METHOD_NOT_ALLOWED,
            detail="Only GET and POST requests are allowed.",
        )

    message = MessageSchema(
        subject=f"Form submission for site '{site.name}'",
        recipients=[EmailStr(site.email)],
        template_body={"name": site.name, "form_data": dict(form_data)},
        subtype=MessageType.html,
    )
    fm = FastMail(request.app.state.email_connection)
    # redirect to the site's redirect URL if it is specified
    if site.redirect_url:
        print("redirecting to", site.redirect_url)
        return RedirectResponse(
            url=site.redirect_url, status_code=status.HTTP_303_SEE_OTHER
        )

    # return {
    #     "message": f"Get form data by slug: {slug}",
    #     "form_data": form_data,
    # }
