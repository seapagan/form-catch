"""Main router for the API.

This will include all the other routers for the API so only this one needs to be
imported by main.
"""
from fastapi import APIRouter

from config.settings import get_settings
from resources import auth, form, home, site, user

router = APIRouter()


router.include_router(home.router)
router.include_router(form.router)

# Only include the site router if we are not in lockdown mode.
# we can also remove routes from the other routers if we want to.
if not get_settings().lockdown:
    router.include_router(site.router)
    router.include_router(auth.router)
    router.include_router(user.router)
