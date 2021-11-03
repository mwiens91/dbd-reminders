"""Gets codes from DBD codes Twitter."""

from typing import Optional
import tweepy
from dbdreminders.constants import DEAD_BY_DAYLIGHT_CODES_TWITTER_ID


def get_codes(
    twitter_api_key: str,
    twitter_api_key_secret: str,
    last_seen_tweet_id: Optional[str] = None,
) -> list[dict]:
    """Returns Tweets containing codes.

    Args:
        twitter_api_key: A string containing a Twitter dev API key.
        twitter_api_key_secret: A string containing a Twitter dev API
            secret.
        last_seen_tweet_id: An optional string containing the last seen
            tweet's ID. If this argument is provided, this function will
            return all the codes from tweets newer than this ID. If not
            provided, this function will only return the latest tweet.

    Returns:
        A list containing dictionaries of Tweets. The dictionaries have
        keys "text" (containing the body of the tweet), "datetime", and
        "id".
    """
    # Set up Twitter api
    auth = tweepy.AppAuthHandler(twitter_api_key, twitter_api_key_secret)
    api = tweepy.API(auth)

    # Get tweet(s)
    if last_seen_tweet_id:
        # Grab all tweets newer than the specified tweet
        tweet_results = api.user_timeline(
            screen_name=DEAD_BY_DAYLIGHT_CODES_TWITTER_ID,
            exclude_replies=True,
            since_id=last_seen_tweet_id,
        )
    else:
        # Grab the latest tweet
        tweet_results = api.user_timeline(
            screen_name=DEAD_BY_DAYLIGHT_CODES_TWITTER_ID,
            exclude_replies=True,
            count=1,
        )

    # Parse the tweets
    tweets = [
        {"text": tweet.text, "datetime": tweet.created_at, "id": tweet.id}
        for tweet in tweet_results
    ]

    return tweets
