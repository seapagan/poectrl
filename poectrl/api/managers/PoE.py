"""Manager for handling the PoE control routes."""
from fastapi import HTTPException

from poectrl.api.settings import get_settings


class PoEManager:
    """Handle the PoE routes."""

    @staticmethod
    def list() -> dict[str, list[str]]:
        """List all the available profiles."""
        profiles = get_settings().profiles
        return {"profiles": list(profiles)}

    @staticmethod
    def show(profile: str):
        """Show details for the chosen profile."""
        profiles = get_settings().profiles
        try:
            this_profile = profiles[profile]
        except KeyError:
            raise HTTPException(
                status_code=404, detail="That Profile does not exist."
            )
        return {profile: this_profile}

    @staticmethod
    def apply(profile: str):
        """Apply the chosen profile."""
