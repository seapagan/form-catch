"""Form data catcher API main module."""
from pathlib import Path

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi_mail import ConnectionConfig
from pydantic import EmailStr

from config.settings import get_settings
from resources import routes

app = FastAPI(
    title="Form Catcher",
    description="This is a simple API to catch form data",
    version="0.1.0",
    swagger_ui_parameters={"defaultModelsExpandDepth": -1},
)


# set up email connection
email_connection = ConnectionConfig(
    MAIL_USERNAME=get_settings().mail_username,
    MAIL_PASSWORD=get_settings().mail_password,
    MAIL_FROM=EmailStr(get_settings().mail_from),
    MAIL_PORT=get_settings().mail_port,
    MAIL_SERVER=get_settings().mail_server,
    MAIL_FROM_NAME=get_settings().mail_from_name,
    MAIL_STARTTLS=get_settings().mail_starttls,
    MAIL_SSL_TLS=get_settings().mail_ssl_tls,
    USE_CREDENTIALS=get_settings().mail_use_credentials,
    VALIDATE_CERTS=get_settings().mail_validate_certs,
    TEMPLATE_FOLDER=Path(__file__).parent / "templates",
)
app.state.email_connection = email_connection


app.include_router(routes.router)
app.mount("/static", StaticFiles(directory="static"), name="static")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)  # nosec
