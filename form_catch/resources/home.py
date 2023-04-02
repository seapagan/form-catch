"""Routes for the home resource."""
from fastapi import APIRouter

router = APIRouter()


@router.get("/")
async def root():
    """Root endpoint to check if the API is running successfully."""
    return {"message": "API running successfully"}
