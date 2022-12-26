"""Define the poe control routes.

These will largely be the same as the respective CLI commands.
"""
from fastapi import APIRouter

from poectrl.api.managers.PoE import PoEManager
from poectrl.api.schemas.response.poe import ApplyResponse, ListResponse

router = APIRouter(tags=["PoE Control"])

poe_ctrl = PoEManager()


@router.get("/list/", response_model=ListResponse)
def list():
    """Return a list of available profiles."""
    return poe_ctrl.list()


@router.get("/show/{profile}")
def show(profile: str):
    """Show info for the specified profile."""
    return poe_ctrl.show(profile)


@router.get("/apply/{profile}", response_model=ApplyResponse)
async def apply(profile: str):
    """Apply the specified profile."""
    return await poe_ctrl.apply(profile)
