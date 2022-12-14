"""Class to control all the CLI commands."""
import json
import subprocess

from rich import print
from rich.panel import Panel

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
            print(
                Panel(
                    "[white]-> No devices are defined. Aborting",
                    title="Error",
                    title_align="left",
                    style="red",
                )
            )
            exit(3)

        self.current_profile = {}

    def read_config(self):
        """Read the entire config file into a dictionary."""
        try:
            return Profile("poectrl.json")
        except MissingConfigurationError:
            print(
                Panel(
                    "[white]-> Cannot find a configuration file. Aborting",
                    title="Error",
                    title_align="left",
                    style="red",
                )
            )
            exit(1)
        except BadConfigurationError:
            print(
                Panel(
                    "[white]-> Invalid configuration file. Aborting",
                    title="Error",
                    title_align="left",
                    style="red",
                )
            )
            exit(2)

    def get_profile(self, profile: str) -> dict:
        """Parse the profile and return as a dict."""
        try:
            this_profile = self.config.get_specific_profile(profile)
        except UnknownProfileError:
            print(
                Panel(
                    "[white]-> That profile does not exist. Aborting",
                    title="Error",
                    title_align="left",
                    style="red",
                )
            )
            quit(3)

        return this_profile

    def activate_profile(self, profile: dict):
        """Activate the specified profile."""
        for device in profile:
            try:
                device_info = self.devices[device]
                poe = PoECtrl(
                    device,
                    device_info["ip"],
                    device_info["user"],
                    device_info["password"],
                )
                poe.process_device(profile[device])
            except KeyError as err:
                print(
                    Panel(
                        f"[white]-> Device {err} has not been defined, skipping.",
                        title="Error",
                        title_align="left",
                        style="red",
                        expand=False,
                    )
                )

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

    def serve(self, reload: bool, port: int):
        """Run the API server using 'gunicorn'."""
        cmd_line = f"uvicorn poectrl.api.main:app --port={port}"
        if reload:
            cmd_line += " --reload"
        subprocess.call(cmd_line, shell=True)
