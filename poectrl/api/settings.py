"""Control the API settings, read from the config file."""

from functools import lru_cache

from pydantic import BaseSettings

from poectrl.profiles import Profile


class Settings(BaseSettings):
    """The Main settings class."""

    # we don't need to wrap this in a try-except since the existence and
    # validity of the config file is checked when running the CLI, before we
    # even get to the API.

    # TODO However, if in future we run the API directly using Gunicorn or
    # similar it will be an issue.
    config: Profile = Profile("poectrl.json")


@lru_cache
def get_settings() -> Profile:
    """Return the settings."""
    return Settings().config
