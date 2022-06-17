"""Contains configuration file related things."""

import os.path
from schema import And, Schema
import yaml
from dbdreminders.constants import (
    CONFIG_FILE_NAME,
    PROJECT_BASE_DIR,
)


class ConfigFileInvalid(Exception):
    """Raised when a config file is invalid."""


class ConfigFileNotFound(Exception):
    """Raised when a config file can't be found."""


def find_config_file() -> str:
    """Find and return the path of a config file.

    The config file looked for is "config.yaml" and it is looked for at
    the base of the repository.

    Returns:
        A string containing the absolute path to the config file.

    Raises:
        ConfigFileNotFound: A config file couldn't be found.
    """
    # Check the base of the project
    config_path = os.path.join(PROJECT_BASE_DIR, CONFIG_FILE_NAME)

    if os.path.exists(config_path):
        return config_path

    # Couldn't find anything
    raise ConfigFileNotFound


def parse_config_file() -> dict[str, str]:
    """Find, parse, and validate a config file.

    Returns:
        A dictionary containing settings in user config file.

    Raises:
        ConfigFileInvalid: A config file wasn't valid.
    """
    # Find the config file first
    config_path = find_config_file()

    # Now parse and return it - note that PyYAML doesn't come with any
    # schema validation, which might be desirable at some point
    with open(config_path, "r") as config_file:
        config_dict = yaml.safe_load(config_file)

    # Build the schema for the config file, and validate what we have
    schema = Schema(
        {
            "gmail-email": And(str, len),
            "gmail-app-password": And(str, len),
            "twitter-api-key": And(str, len),
            "twitter-api-key-secret": And(str, len),
            "users": [
                {
                    "email": str,
                    "notify-about-codes": bool,
                    "perks-to-notify-about": [str],
                }
            ],
        }
    )

    if not schema.is_valid(config_dict):
        raise ConfigFileInvalid

    return config_dict
