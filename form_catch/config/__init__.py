"""Control the app settings, including reading from a .env file."""
from functools import lru_cache

from pydantic import BaseSettings


class Settings(BaseSettings):
    """Main Settings class.

    This allows to set some defaults, that can be overwritten from the .env
    file if it exists.
    Do NOT put passwords and similar in here, use the .env file instead, it will
    not be stored in the Git repository.
    """

    base_url: str = "http://localhost:8000"

    cors_origins: str = "*"

    # Setup the Postgresql database.
    db_user = "my_db_username"
    db_password = "Sup3rS3cr3tP455w0rd"
    db_address = "localhost"
    db_port = "5432"
    db_name = "api-template"

    class Config:
        """Override the default variables from an .env file, if it exists."""

        env_file = ".env"


@lru_cache
def get_settings() -> Settings:
    """Return the current settings."""
    return Settings()
