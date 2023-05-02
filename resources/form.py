"""Routes for handling form data."""
from fastapi import (
    APIRouter,
    BackgroundTasks,
    Depends,
    HTTPException,
    Request,
    status,
)
from fastapi.responses import RedirectResponse
from fastapi_mail import FastMail, MessageSchema, MessageType
from fastapi_mail.errors import ConnectionErrors
from pydantic import EmailStr

from database.db import get_database
from helpers.slug import get_site_by_slug

router = APIRouter(prefix="/form", tags=["Form Handling"])


async def send_mail_task(fm: FastMail, message: MessageSchema):
    """Send the email in the background."""
    try:
        await fm.send_message(message, template_name="submission.html")
    except ConnectionErrors as e:
        # later we will actually log this error
        print("Error sending email:", str(e))


async def get_form_data(request: Request):
    """Get the form data from the request.

    This function is used to get the form data from the request. It is used
    in the echo_form route and the respond_to_form route.
    """
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
    return form_data


@router.get("/echo", response_model=dict[str, str])
@router.post("/echo", response_model=dict[str, str])
async def echo_form(request: Request):
    """Echo the form data back to the user.

    This is useful during development to see what data is being sent to the
    server.

    Note that this route responds to both GET and POST requests.
    """
    form_data = await get_form_data(request)

    return dict(form_data)


@router.get("/{slug}", status_code=status.HTTP_204_NO_CONTENT)
@router.post("/{slug}", status_code=status.HTTP_204_NO_CONTENT)
async def respond_to_form(
    slug: str,
    request: Request,
    backgroundtasks: BackgroundTasks,
    db=Depends(get_database),
):
    """Get the supplied form data and email it.

    Note that the slug is used to determine the email address to send the form
    data to.

    Also, this route responds to both GET and POST requests.
    """
    site = await get_site_by_slug(slug, db)
    if not site:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Site not found."
        )

    # Get the form data depending on the request method
    form_data = await get_form_data(request)

    # Check that the form data is not empty
    if len([x for x in form_data.values() if x]) == 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No form data was supplied.",
        )

    # Send the email
    message = MessageSchema(
        subject=f"Form submission for site '{site['name']}'",
        recipients=[EmailStr(site["email"])],
        template_body={"name": site["name"], "form_data": dict(form_data)},
        subtype=MessageType.html,
    )
    fm = FastMail(request.app.state.email_connection)
    backgroundtasks.add_task(send_mail_task, fm, message)

    # redirect to the site's redirect URL if it is specified
    if site["redirect_url"]:
        print("redirecting to", site["redirect_url"])
        return RedirectResponse(
            url=site["redirect_url"], status_code=status.HTTP_303_SEE_OTHER
        )
