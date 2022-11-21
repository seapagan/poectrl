"""Control the use of Profile files for the PoECtrl library."""
import json
from pathlib import Path

from rich import print

from .errors import (
    BadConfigurationError,
    MissingConfigurationError,
    NoDevicesError,
    NoProfilesError,
    UnknownProfileError,
)


class Profile:
    """Read profiles and devices from a configuration file."""

    def __init__(self, filename):
        """Initialize the class."""
        self.filename = filename
        self.local_config_file = Path.cwd() / Path(filename)
        self.home_config_file = Path.home() / Path(filename)

        self.absolute_filename = self.get_config_filename()

        self.config = self.read_config()
        self.devices = self.get_devices()
        self.profiles = self.get_profiles()

    def get_config_filename(self):
        """Return the full path to the configuration file."""
        if self.local_config_file.exists():
            return self.local_config_file
        elif self.home_config_file.exists():
            return self.home_config_file
        else:
            raise MissingConfigurationError

    def read_config(self):
        """Return the configuration file as a dictionary."""
        try:
            print(f"[green]Using configuration from {self.absolute_filename}")
            with open(self.absolute_filename) as f:
                return json.load(f)
        except json.JSONDecodeError:
            raise BadConfigurationError

    def get_devices(self):
        """Return a dictionary with only the defined devices."""
        try:
            return self.config["devices"]
        except KeyError:
            raise NoDevicesError

    def get_profiles(self):
        """Return a dictionary with only the defined profiles."""
        try:
            return self.config["profiles"]
        except KeyError:
            raise NoProfilesError

    def get_specific_profile(self, profile_name):
        """Return the details for a specific profile."""
        try:
            return self.profiles[profile_name]
        except KeyError:
            raise UnknownProfileError
