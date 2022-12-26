"""Manager for handling the PoE control routes."""
from fastapi import HTTPException, status

from poectrl.api.settings import get_settings
from poectrl.base import PoECtrl


class PoEManager:
    """Handle the PoE routes."""

    def __init__(self):
        """Initialize the class."""
        self.profiles = get_settings().profiles
        self.devices = get_settings().devices

    def list(self) -> dict[str, list[str]]:
        """List all the available profiles."""
        return {"profiles": list(self.profiles)}

    def show(self, profile: str):
        """Show details for the chosen profile."""
        try:
            this_profile = self.profiles[profile]
        except KeyError:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="That Profile does not exist",
            )
        return {profile: this_profile}

    async def apply(self, profile: str):
        """Apply the chosen profile."""
        try:
            this_profile = self.profiles[profile]
        except KeyError:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="That Profile does not exist",
            )

        for device_name, device_profile in this_profile.items():
            try:
                device_info = self.devices[device_name]
                poe = PoECtrl(
                    device_name,
                    device_info["ip"],
                    device_info["user"],
                    device_info["password"],
                )
                poe.api_process_device(device_profile)
            except KeyError:
                # this device does not exist. we will be less forgiving than the
                # CLI app and abort the operation.
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Device {device_name} is not configured",
                )

        return {"detail": f"Profile '{profile}' Applied"}
