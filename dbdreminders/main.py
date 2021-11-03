"""Contains the main function."""

import sys
from dbdreminders.cache import (
    CacheFileInvalid,
    CacheFileNotFound,
    save_cache_file,
    parse_cache_file,
)
from dbdreminders.codes import get_codes
from dbdreminders.configuration import (
    ConfigFileInvalid,
    ConfigFileNotFound,
    parse_config_file,
)
from dbdreminders.email import send_email
from dbdreminders.perks import get_perks


def main():
    """The main function."""
    # Read config file
    try:
        config_dict = parse_config_file()
    except ConfigFileNotFound:
        print("Config file not found. Aborting.")
        sys.exit(1)
    except ConfigFileInvalid:
        print("Config file invalid. Aborting.")
        sys.exit(1)

    # Read cache file if it exists
    try:
        cache_dict = parse_cache_file()
        first_run = False
    except CacheFileNotFound:
        print("Cache file not found. Creating a new one.")
        first_run = True
    except CacheFileInvalid:
        print("Cache file invalid. Aborting.")
        sys.exit(1)

    # Get the current perks and code tweets
    perks_results = get_perks()

    if first_run:
        tweets_results = get_codes(
            config_dict["twitter-api-key"],
            config_dict["twitter-api-key-secret"],
        )
    else:
        tweets_results = get_codes(
            config_dict["twitter-api-key"],
            config_dict["twitter-api-key-secret"],
            cache_dict["last-tweet-seen"],
        )

    perks_set = set(perks_results)

    # Create the cache if necessary/update existing one if necessary.
    # The logic with what is changed or not is a little complicated,
    # but it shouldn't be too hard to figure out. Basically if we mark
    # something as changed then that's a flag to notify about that
    # thing.
    tweet_changed = False
    perks_changed = False

    if first_run:
        new_cache_dict = {
            "last-tweet-seen": tweets_results[0]["id"],
            "last-perks-seen": perks_set,
        }
        perks_changed = True
    else:
        new_cache_dict = {}

        if tweets_results:
            new_cache_dict["last-tweet-seen"] = tweets_results[0]["id"]
            tweet_changed = True
        else:
            new_cache_dict["last-tweet-seen"] = cache_dict["last-tweet-seen"]

        if perks_set != cache_dict["last-perks-seen"]:
            new_cache_dict["last-perks-seen"] = perks_set
            perks_changed = True
        else:
            new_cache_dict["last-perks-seen"] = cache_dict["last-perks-seen"]

    if tweet_changed:
        tweets = "**New code tweets**\n\n" + "\n".join(
            [
                str(tweet["datetime"]) + "\n\n" + tweet["text"] + "\n"
                for tweet in tweets_results
            ]
        ).rstrip("\n")
    else:
        tweets = None

    # Send email to relevant users
    for user_dict in config_dict["users"]:
        # Build the message based on what we need to send
        message = ""

        if perks_changed:
            perks_to_notify_about = perks_set.intersection(
                set(user_dict["perks-to-notify-about"])
            )
        else:
            perks_to_notify_about = {}

        if tweets and user_dict["notify-about-codes"]:
            message += tweets

            if perks_to_notify_about:
                message += "\n\n"

        if perks_to_notify_about:
            message += (
                "**Perks that you care about are available!**\n\n"
                + "\n".join(
                    ["- " + perk for perk in perks_to_notify_about]
                ).rstrip("\n")
            )

        # Build the subject string
        if perks_to_notify_about:
            if tweets:
                subject = ("Dead by Daylight codes and perks available!",)
            else:
                subject = ("Dead by Daylight perks available!",)
        else:
            if tweets:
                subject = ("Dead by Daylight codes available!",)
            else:
                subject = ""

        # Send the email if there's anything to send
        if message:
            send_email(
                config_dict["gmail-username"],
                config_dict["gmail-password"],
                [user_dict["email"]],
                subject,
                message,
            )

            print("email sent to %s" % user_dict["email"])

    # Save the cache
    save_cache_file(new_cache_dict)
