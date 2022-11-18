"""Define Error Handlers for the PoECtrl class."""


class CannotConnectError(Exception):
    """Raised when we cannot connect to a device."""


class BadAuthenticationError(Exception):
    """Raised if the user/pass is incorrect."""
