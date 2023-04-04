"""Define schemas used to send email."""
from pydantic import BaseModel, EmailStr


class EmailSchema(BaseModel):
    """Define schema for email data."""

    email: EmailStr
    subject: str
    body: str
