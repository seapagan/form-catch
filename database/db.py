"""Set up the database connection."""
import databases
import sqlalchemy

from config.settings import get_settings

DATABASE_URL = (
    f"postgresql://{get_settings().db_user}:{get_settings().db_password}@"
    f"{get_settings().db_address}:{get_settings().db_port}/"
    f"{get_settings().db_name}"
)

database = databases.Database(DATABASE_URL)
metadata = sqlalchemy.MetaData()


def get_database():
    """Return the database connection."""
    return database
