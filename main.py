# main FastAPI contorl file.
from fastapi import FastAPI

app= FastAPI(
    title="Form data catcher",
    description="This is a simple API to catch form data",
    version="0.1.0",
)


@app.get("/")
async def root():
    return {"message": "API running successfully"}
