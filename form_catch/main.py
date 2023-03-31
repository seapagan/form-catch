# main FastAPI contorl file.
from fastapi import FastAPI

from form_catch.database.db import database

app= FastAPI(
    title="Form data catcher",
    description="This is a simple API to catch form data",
    version="0.1.0",
)
app.state.database = database

@app.get("/")
async def root():
    return {"message": "API running successfully"}


# ------ Init and close the database connection on startup and shutdown. ----- #
@app.on_event("startup")
async def startup() -> None:
    database_ = app.state.database
    if not database_.is_connected:
        await database_.connect()


@app.on_event("shutdown")
async def shutdown() -> None:
    database_ = app.state.database
    if database_.is_connected:
        await database_.disconnect()
