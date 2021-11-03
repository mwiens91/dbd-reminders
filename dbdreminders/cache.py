"""Contains cache file related things."""

import os.path
import sys
from schema import And, Schema
import yaml
from dbdreminders.codes import get_codes
from dbdreminders.constants import (
    CACHE_FILE_NAME,
    PROJECT_BASE_DIR,
)


class CacheFileInvalid(Exception):
    """Raised when a config file is invalid."""


class CacheFileNotFound(Exception):
    """Raised when a config file can't be found."""


def find_cache_file() -> str:
    """Find and return the path of a config file.

    The config file looked for is "cache.yaml" and it is looked for at
    the base of the repository.

    Returns:
        A string containing the absolute path to the cache file.

    Raises:
        CacheFileNotFound: A cache file couldn't be found.
    """
    # Check the base of the project
    cache_path = os.path.join(PROJECT_BASE_DIR, CACHE_FILE_NAME)

    if os.path.exists(cache_path):
        return cache_path

    # Couldn't find anything
    raise CacheFileNotFound


def parse_cache_file() -> dict:
    """Find, parse, and validate a cache file.

    Returns:
        A dictionary containing settings in user cache file.

    Raises:
        CacheFileInvalid: A cache file wasn't valid.
    """
    # Find the config file first
    cache_path = find_cache_file()

    # Now parse and return it - note that PyYAML doesn't come with any
    # schema validation, which might be desirable at some point
    with open(cache_path, "r") as cache_file:
        cache_dict = yaml.safe_load(cache_file)

    # Build the schema for the config file, and validate what we have
    schema = Schema(
        {
            "last-tweet-seen": And(int, lambda x: x > 0),
            "last-perks-seen": And({str}, len),
        }
    )

    if not schema.is_valid(cache_dict):
        raise CacheFileInvalid

    return cache_dict


def save_cache_file(cache_dict: dict):
    """Save a cache file

    Arg:
        cache_dict: A dictionary containing the data to save.
    """
    # The path of the cache file
    cache_path = os.path.join(PROJECT_BASE_DIR, CACHE_FILE_NAME)

    with open(cache_path, "w") as cache_file:
        yaml.dump(cache_dict, cache_file)
