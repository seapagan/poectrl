"""Define the poe control routes.

These will largely be the same as the respective CLI commands.
"""
from fastapi import APIRouter

router = APIRouter()


@router.get("/list/")
def list():
    """Return a list of available profiles."""


@router.get("/show/{profile}")
def show(profile: str):
    """Show info for the specified profile."""
    return {"show": profile}


@router.get("/apply/{profile}")
def apply(profile: str):
    """Apply the specified profile."""
    return {"apply": profile}
