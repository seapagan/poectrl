"""Define the poe control routes.

These will largely be the same as the respective CLI commands.
"""
from fastapi import APIRouter

from poectrl.api.managers.PoE import PoEManager
from poectrl.api.schemas.response.poe import ListResponse

router = APIRouter(tags=["PoE Control"])


@router.get("/list/", response_model=ListResponse)
def list():
    """Return a list of available profiles."""
    return PoEManager.list()


@router.get("/show/{profile}")
def show(profile: str):
    """Show info for the specified profile."""
    return PoEManager.show(profile)


@router.get("/apply/{profile}")
def apply(profile: str):
    """Apply the specified profile."""
    return PoEManager.apply(profile)
