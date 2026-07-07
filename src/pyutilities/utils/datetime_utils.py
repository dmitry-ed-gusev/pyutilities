# -*- coding: utf-8 -*-

"""
Useful date/time utilities and functions.

Created:  Dmitrii Gusev, 22.03.2026
Modified: Dmitrii Gusev, 07.07.2026
"""

import calendar
import logging
from datetime import datetime, timedelta, timezone
from functools import lru_cache

from pyutilities.defaults import MSG_MODULE_ISNT_RUNNABLE

# DATETIME :: timezones defaults
MSK_TIMEZONE_NAME: str = "Moscow TZ (GMT+3)"
MSK_TIMEZONE: timezone = timezone(timedelta(hours=3), name=MSK_TIMEZONE_NAME)
# - CACHE :: cache setup (size) for cached functions/methods
LRU_CACHE_SIZE: int = 128


log = logging.getLogger(__name__)
log.addHandler(logging.NullHandler())


def shift_timestamp(base_timestamp: datetime, delta_years: float = 0, delta_months: float = 0,
                    delta_days: float = 0, delta_hours: float = 0, delta_minutes: float = 0,
                    delta_seconds: float = 0, trace: bool = False) -> datetime:
    """Shifts the provided timestamp by the specified delta (in years / months / days / hours / minutes
    / seconds). Return timestamp."""

    if not base_timestamp:
        return None

    # get parts of the base timestamp
    year: int = base_timestamp.year  # get year
    month: int = base_timestamp.month  # get month
    day: int = base_timestamp.day  # get day
    hour: int = base_timestamp.hour  # get hour
    minute: int = base_timestamp.minute  # get minute
    second: int = base_timestamp.second  # get second

    # adjust YEAR according to delta
    if delta_years != 0:
        year += delta_years

    # adjust MONTH + YEAR (if necessary)
    if delta_months != 0:
        month += delta_months
        if abs(month) > 12:  # adding year(s) (roll over several months)
            year += month // 12
            month += month % 12
        elif abs(month) < 1:  # subtracting year (month = 0 -> previous year, december)
            year -= 1
            month = 12
        else:  # 1 <= abs(month) <= 12. but may be negative
            if month < 0:
                year -= 1
                month = 12 + month

    result: datetime = datetime(year, month, day, hour, minute, second) + \
        timedelta(days=delta_days, hours=delta_hours, minutes=delta_minutes, seconds=delta_seconds)

    if trace:
        log.debug("Generated from [%s] timestamp [%s].", base_timestamp, result)

    return result


@lru_cache(maxsize=LRU_CACHE_SIZE)
def shift_timestampc(base_timestamp: datetime, delta_years: float = 0, delta_months: float = 0,
                     delta_days: float = 0, delta_hours: float = 0, delta_minutes: float = 0,
                     delta_seconds: float = 0, trace: bool = False) -> datetime:
    """CASHED version of the shift_timestamp() method. Shifts the provided timestamp by the specified
    delta (in years / months / days / hours / minutes / seconds). Return timestamp."""

    return shift_timestamp(base_timestamp, delta_years, delta_months, delta_days, delta_hours,
                           delta_minutes, delta_seconds, trace)


def get_shifted_timestamp(current_timezone: timezone = MSK_TIMEZONE, delta_years: int = 0,
                          delta_months: int = 0, delta_days: float = 0, delta_hours: float = 0,
                          delta_minutes: float = 0, delta_seconds: float = 0,
                          trace: bool = False) -> datetime:
    """Return the current timestamp with delta: now (in the default timezone) +/- the specified time delta
    in years / months / days / hours / minutes / seconds. Default timezone can be changed by the function
    argument."""

    # generate the current timestamp
    current_timestamp: datetime = datetime.now(current_timezone) if current_timezone else datetime.now()

    return shift_timestamp(current_timestamp, delta_years, delta_months, delta_days, delta_hours,
                           delta_minutes, delta_seconds, trace)


@lru_cache(maxsize=LRU_CACHE_SIZE)
def get_shifted_timestampc(current_timezone: timezone = MSK_TIMEZONE, delta_years: int = 0,
                           delta_months: int = 0, delta_days: float = 0, delta_hours: float = 0,
                           delta_minutes: float = 0, delta_seconds: float = 0,
                           trace: bool = False) -> datetime:
    """CACHED. Cached version of the get_timestamp() method."""

    return get_shifted_timestamp(current_timezone, delta_years, delta_months, delta_days, delta_hours,
                                 delta_minutes, delta_seconds, trace)


def get_dates_range_before_date(date: datetime, tzinfo: timezone) -> tuple[int, int]:
    """Generates two dates range - date_from/date_to for the time period 'before today' - from the 1st day
    of the current month till the today - 1 day (current month). In case today is 1st day - range for the
    whole previous month, if today is 01.01.XXXX - range for 01.12.XXXX-1 - 31.12.XXXX-1.
    """

    log.debug("get_dates_range_before_date(): the date [%s].", date)

    tstamp_from: int = 0
    tstamp_to: int = 0

    if date:  # if date is OK (not empty/None)

        # - processing and calculating dates
        if date.day == 1:  # today - 1st day of month, we need report for the previous month

            if date.month == 1:  # we are at 01.01.XXXX - we need report for Dec.XXXX - 1

                date_from = datetime(date.year - 1, 12, 1, tzinfo=tzinfo)  # from: 01 Dec Year-1 (prev. year)
                date_to = datetime(date.year - 1, 12, 31, tzinfo=tzinfo)  # to: 31 Dec Year-1 (prev. year)

            else:  # we are at 01.XX.XXXX - we need report for previous month

                # from: 01 Month-1 Year
                date_from = datetime(date.year, date.month - 1, 1, tzinfo=tzinfo)
                # last day of the previous month
                _, last_day = calendar.monthrange(date.year, date.month - 1)
                # to: Last Day Month-1 Year
                date_to = datetime(date.year, date.month - 1, last_day, tzinfo=tzinfo)

        else:  # today isn't the 1st, we need report from 1st till yesterday

            date_from = datetime(date.year, date.month, 1, tzinfo=tzinfo)  # from: 01 Month Year
            date_to = datetime(date.year, date.month, date.day - 1, tzinfo=tzinfo)  # to: Day-1 Month Year

        # - final date/time - date from: XX.XX.XX 00:00:00
        tstamp_from = int(
            datetime(
                date_from.year, date_from.month, date_from.day, hour=0, minute=0, second=0, tzinfo=tzinfo
            ).timestamp()
        )
        # - final date/time - # date to: XX.XX.XXXX 23:59:59
        tstamp_to = int(
            datetime(
                date_to.year, date_to.month, date_to.day, hour=23, minute=59, second=59, tzinfo=tzinfo
            ).timestamp()
        )

    log.debug("Timestamps for [%s]: from [%s], to [%s].", date, tstamp_from, tstamp_to)

    # - return the tuple of values
    return (tstamp_from, tstamp_to)


@lru_cache(maxsize=LRU_CACHE_SIZE)
def get_dates_range_before_datec(date: datetime, tzinfo: timezone) -> tuple[int, int]:
    """CACHED. Cached version of the get_dates_range_before_date()."""

    return get_dates_range_before_date(date, tzinfo)


def human_readable_duration_seconds(duration_seconds):
    """Convert duration in seconds into human-readable string-duration."""

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
