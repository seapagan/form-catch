"""Define schemas for the Form response handling."""

from pydantic import BaseModel


class EchoResponse(BaseModel):
    """Define schema for the form 'echo' test route."""

    form_data: dict[str, str]
