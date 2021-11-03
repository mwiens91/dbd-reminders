"""Gets perks from DBD Fandom wiki."""

import fandom
from dbdreminders.constants import (
    DEAD_BY_DAYLIGHT_FANDOM_WIKI,
    DEAD_BY_DAYLIGHT_SHRINE_OF_SECRETS_PAGE_TITLE,
    DEAD_BY_DAYLIGHT_SHRINE_OF_SECRETS_PERKS_SECTION,
)


def get_perks() -> list[str]:
    """Returns a list of strings containing perks in the Shrine of Secrets."""
    # Get current perks offered in Shrine of Secrets
    page = fandom.page(
        title=DEAD_BY_DAYLIGHT_SHRINE_OF_SECRETS_PAGE_TITLE,
        wiki=DEAD_BY_DAYLIGHT_FANDOM_WIKI,
    )
    section_str = page.section(
        DEAD_BY_DAYLIGHT_SHRINE_OF_SECRETS_PERKS_SECTION
    )

    # Parse which perks are available according to schema
    section_list = section_str.split("\n")
    perks = [
        section_list[4],
        section_list[7],
        section_list[10],
        section_list[13],
    ]

    return perks
