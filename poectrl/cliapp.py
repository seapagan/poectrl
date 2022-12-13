"""Class to control all the CLI commands."""
import json

from rich import print

from .base import PoECtrl
from .errors import (
    BadConfigurationError,
    MissingConfigurationError,
    NoDevicesError,
    UnknownProfileError,
)
from .profiles import Profile


class CLIApp:
    """Main CLI loop class."""

    def __init__(self):
        """Initialize the class."""
        self.config = self.read_config()

        try:
            self.profiles = self.config.get_profiles()
            self.devices = self.config.get_devices()
        except NoDevicesError:
            print("[red]-> No devices are defined. Aborting")
            exit(3)

        self.current_profile = {}

    def read_config(self):
        """Read the entire config file into a dictionary."""
        try:
            return Profile("poectrl.json")
        except MissingConfigurationError:
            print("[red]-> Cannot find a configuration file. Aborting")
            exit(1)
        except BadConfigurationError:
            print("[red]-> Invalid configuration file. Aborting")
            exit(2)

    def get_profile(self, profile: str) -> dict:
        """Parse the profile and return as a dict."""
        try:
            this_profile = self.config.get_specific_profile(profile)
        except UnknownProfileError:
            print("[red]-> That profile does not exist. Aborting")
            quit(3)

        return this_profile

    def activate_profile(self, profile: dict):
        """Activate the specified profile."""
        for device in profile:
            try:
                auth = self.devices[device]
                poe = PoECtrl(device, auth["user"], auth["password"])
                poe.process_device(profile[device])
            except KeyError as err:
                print(f"[red]-> Device {err} has not been defined, skipping.")

    def list(self):
        """List all the available profiles."""
        print("\nValid profiles are :")
        for profile in self.profiles:
            print(f"[green] - {profile}")

    def show(self, profile):
        """Show details of a specific profile."""
        this_profile = self.get_profile(profile)
        # this is just a temp placeholder, I'll write a prettier one later.
        print(json.dumps(this_profile, indent=4))

    def apply(self, profile_name: str):
        """Apply the specified profile.

        Turn PoE ports on/off depending on the settings in the Profile.
        """
        this_profile = self.get_profile(profile_name)
        self.activate_profile(this_profile)
