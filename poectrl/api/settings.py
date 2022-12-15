"""Control the API settings, read from the config file."""

from functools import lru_cache

from pydantic import BaseSettings

from poectrl.profiles import Profile


class Settings(BaseSettings):
    """The Main settings class."""

    config: Profile = Profile("poectrl.json")


@lru_cache
def get_settings() -> Profile:
    """Return the settings."""
    return Settings().config
