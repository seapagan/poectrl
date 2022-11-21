"""Define Error Handlers for the PoECtrl class."""


class CannotConnectError(Exception):
    """Raised when we cannot connect to a device."""


class BadAuthenticationError(Exception):
    """Raised if the user/pass is incorrect."""


class CannotReadSettingsError(Exception):
    """Raised if the device settings cannot be read."""


class CannotWriteSettingsError(Exception):
    """Raised if the device settings cannot be written."""


class MissingConfigurationError(Exception):
    """Raised if the configuration file cannot be found."""


class BadConfigurationError(Exception):
    """Raised if the configuration file cannot be decoded."""


class UnknownProfileError(Exception):
    """Raised if the specified profile does not exist."""


class NoDevicesError(Exception):
    """Raised if no devices are defined."""


class NoProfilesError(Exception):
    """Raised if no profiles are defined."""
