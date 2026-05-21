# -*- coding: utf-8 -*-

"""
Useful date/time utilities and functions.

Created:  Dmitrii Gusev, 22.03.2026
Modified: Dmitrii Gusev, 21.05.2026
"""

import logging
from functools import lru_cache
from datetime import datetime, timedelta, timezone

import pendulum
from pendulum import Date

from pyutilities.defaults import MSG_MODULE_ISNT_RUNNABLE

# DATETIME :: timezones defaults
MSK_TIMEZONE: timezone = timezone(timedelta(hours=3), name="Moscow Timezone (GMT+3)")
MSK_TIMEZONE_NAME: str = "Europe/Moscow"
# - CACHE :: cache setup (size) for cached functions/methods
LRU_CACHE_SIZE: int = 128


log = logging.getLogger(__name__)
log.addHandler(logging.NullHandler())


def get_timestamp(current_timezone: timezone = MSK_TIMEZONE, days: float = 0, hours: float = 0,
                  minutes: float = 0, seconds: float = 0, ) -> datetime:
    """Return timestamp: now (in the default timezone) +/- the specified time delta in hours / minutes /
    seconds. Default timezone can be changed by the function argument."""

    return datetime.now(current_timezone) + timedelta(
        days=days, hours=hours, minutes=minutes, seconds=seconds
    )


@lru_cache(maxsize=LRU_CACHE_SIZE)
def get_timestampc(current_timezone: timezone = MSK_TIMEZONE, days: float = 0, hours: float = 0,
                   minutes: float = 0, seconds: float = 0, ) -> datetime:
    """CACHED. Cached version of the get_timestamp() method."""

    return get_timestamp(current_timezone, days, hours, minutes, seconds)


def get_dates_range_before_date(date: datetime) -> tuple[int, int]:
    """Generates two dates range - date_from/date_to for the time period 'before today' - from the 1st day
    of the current month till the today - 1 day (current month). In case today is 1st day - range for the
    whole previous month, if today is 01.01.XXXX - range for 01.12.XXXX-1 - 31.12.XXXX-1.
    """

    log.debug("get_dates_range_before_date(): the date [%s].", date)

    # - local variables
    local_today: Date = Date(date.year, date.month, date.day)
    date_from: Date
    date_to: Date

    # - processing and calculating dates
    if local_today.day == 1:  # today - 1st day of month, we need report for the previous month

        if local_today.month == 1:  # we are at 01.01.XXXX - we need report for Dec.XXXX - 1

            date_from = pendulum.date(local_today.year - 1, 12, 1)  # from: 01 Dec Year-1
            date_to = pendulum.date(local_today.year - 1, 12, 31)  # to: 31 Dec Year-1

        else:  # we are at 01.XX.XXXX - we need report for previous month

            # from: 01 Month-1 Year
            date_from = pendulum.date(local_today.year, local_today.month - 1, 1)
            # to: Last Day Month-1 Year
            date_to = pendulum.date(
                local_today.year, local_today.month - 1, local_today.subtract(months=1).days_in_month
            )

    else:  # today isn't the 1st, we need report from 1st till yesterday

        date_from = pendulum.date(local_today.year, local_today.month, 1)  # from: 01 Month Year
        date_to = pendulum.date(local_today.year, local_today.month, date.day - 1)  # to: Day-1 Month Year

    # - generate from/to timestamps
    tstamp_from = pendulum.datetime(date_from.year, date_from.month, date_from.day,
                                    hour=0, minute=0, second=0)  # date from: XX.XX.XX 00:00:00
    tstamp_to = pendulum.datetime(date_to.year, date_to.month, date_to.day,
                                  hour=23, minute=59, second=59)  # date to: XX.XX.XXXX 23:59:59
    log.debug("Generated timestamps: from [%s], to [%s].", tstamp_from, tstamp_to)

    # - return the tuple of values
    return (tstamp_from.int_timestamp, tstamp_to.int_timestamp)


@lru_cache(maxsize=LRU_CACHE_SIZE)
def get_dates_range_before_datec(date: datetime) -> tuple[int, int]:
    """CACHED. Cached version of the get_dates_range_before_date()."""

    return get_dates_range_before_date(date)


def human_readable_duration_seconds(duration_seconds):
    """Convert duration in seconds into human-readable string-duration.
    """

    days = duration_seconds // (24 * 3600)
    hours = (duration_seconds % (24 * 3600)) // 3600
    minutes = (duration_seconds % (24 * 3600)) % 3600 // 60
    seconds = duration_seconds % 3600 % 60

    result = ""
    if days > 0:
        result += f"{days} д. "
    if hours > 0:
        result += f"{hours} ч. "
    if minutes > 0:
        result += f"{minutes:02d} мин. "
    result += f"{seconds:02d} сек."
    result = result.strip()

    log.debug("Converted duration: [%s] into readable str: [%s].", duration_seconds, result)

    return result


@lru_cache(maxsize=LRU_CACHE_SIZE)
def human_readable_duration_secondsc(duration_seconds):
    """CACHED. Cached version of the human_readable_duration_seconds() method."""

    return human_readable_duration_seconds(duration_seconds)


if __name__ == "__main__":
    print(MSG_MODULE_ISNT_RUNNABLE)
