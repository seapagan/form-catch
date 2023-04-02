"""Main router for the API.

This will include all the other routers for the API so only this one needs to be
imported by main.
"""
from fastapi import APIRouter

from form_catch.resources import form, home, site

router = APIRouter()

router.include_router(home.router)
router.include_router(form.router)
router.include_router(site.router)
