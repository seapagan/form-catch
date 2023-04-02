"""Form data catcher API main module."""
from fastapi import FastAPI

from form_catch.database.db import database

app = FastAPI(
    title="Form data catcher",
    description="This is a simple API to catch form data",
    version="0.1.0",
)
app.state.database = database


@app.get("/")
async def root():
    """Root endpoint to check if the API is running successfully."""
    return {"message": "API running successfully"}


# ------ Init and close the database connection on startup and shutdown. ----- #
@app.on_event("startup")
async def startup() -> None:
    """Connect to the database on startup."""
    database_ = app.state.database
    if not database_.is_connected:
        await database_.connect()


@app.on_event("shutdown")
async def shutdown() -> None:
    """Disconnect from the database on shutdown."""
    database_ = app.state.database
    if database_.is_connected:
        await database_.disconnect()
