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

from dateutil.relativedelta import relativedelta

from pyutilities.defaults import MSG_MODULE_ISNT_RUNNABLE

# DATETIME :: timezones defaults
MSK_TIMEZONE_NAME: str = "Moscow TZ (GMT+3)"
MSK_TIMEZONE: timezone = timezone(timedelta(hours=3), name=MSK_TIMEZONE_NAME)
# - CACHE :: cache setup (size) for cached functions/methods
LRU_CACHE_SIZE: int = 128


log = logging.getLogger(__name__)
log.addHandler(logging.NullHandler())


def shift_timestamp(base_timestamp: datetime, delta_years: int = 0, delta_months: int = 0,
                    delta_days: float = 0, delta_hours: float = 0, delta_minutes: float = 0,
                    delta_seconds: float = 0, trace: bool = False) -> datetime | None:
    """Shifts the provided timestamp by the specified delta (in years / months / days / hours / minutes
    / seconds). Return timestamp."""

    if not base_timestamp:  # fast-check/fail-fast
        return None

    # Использование relativedelta решает проблему некорректных дней (например, 31 февраля)
    # и делает это атомарно для лет/месяцев.
    result: datetime
    try:
        # 1. Смещаем года и месяцы
        result = base_timestamp + relativedelta(years=delta_years, months=delta_months)

        # 2. Смещаем дробные/стандартные дни, часы, минуты и секунды
        result += timedelta(days=delta_days, hours=delta_hours, minutes=delta_minutes, seconds=delta_seconds)

        # 3. Нормализуем таймзону (важно для DST границ)
        if result.tzinfo is not None:
            result = result.astimezone(result.tzinfo)

    except (ValueError, OverflowError):
        # Защита от выхода за пределы поддерживаемых дат Python (года 1-9999)
        return None

    if trace:
        log.debug("Generated from [%s] timestamp [%s].", base_timestamp, result)

    return result


@lru_cache(maxsize=LRU_CACHE_SIZE)
def shift_timestampc(base_timestamp: datetime, delta_years: int = 0, delta_months: int = 0,
                     delta_days: float = 0, delta_hours: float = 0, delta_minutes: float = 0,
                     delta_seconds: float = 0, trace: bool = False) -> datetime | None:
    """CASHED version of the shift_timestamp() method. Shifts the provided timestamp by the specified
    delta (in years / months / days / hours / minutes / seconds). Return timestamp."""

    return shift_timestamp(base_timestamp, delta_years, delta_months, delta_days, delta_hours,
                           delta_minutes, delta_seconds, trace)


def get_shifted_timestamp(current_timezone: timezone = MSK_TIMEZONE, delta_years: int = 0,
                          delta_months: int = 0, delta_days: float = 0, delta_hours: float = 0,
                          delta_minutes: float = 0, delta_seconds: float = 0,
                          trace: bool = False) -> datetime | None:
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
                           trace: bool = False) -> datetime | None:
    """CACHED. Cached version of the get_timestamp() method."""

    return get_shifted_timestamp(current_timezone, delta_years, delta_months, delta_days, delta_hours,
                                 delta_minutes, delta_seconds, trace)


def get_str_month(dt: datetime,
                  month_number_prefix: bool = True,
                  year_number_postfix: bool = False,
                  delimiter: str = ".") -> str:
    """Return string name of the month with variations, for utility usage (folders names etc.)"""

    prefix: str = ""
    postfix: str = ""
    if month_number_prefix:
        prefix = f"{dt.month:02d}{delimiter}"
    if year_number_postfix:
        postfix = f"{delimiter}{dt.year}"

    return f"{prefix}{calendar.month_name[dt.month]}{postfix}"


def get_str_current_month():
    return get_str_month(datetime.now(tz=MSK_TIMEZONE))


def get_str_prev_month():
    return get_str_month(get_shifted_timestamp(delta_months=-1))


def get_str_next_month():
    return get_str_month(get_shifted_timestamp(delta_months=1))


def get_dates_range_before_date(date: datetime, tzinfo: timezone) -> tuple[int, int]:
    """Generates two dates range - date_from/date_to for the time period 'before today' - from the 1st day
    of the current month till the today - 1 day (current month). In case today is 1st day - range for the
    whole previous month, if today is 01.01.XXXX - range for 01.12.XXXX-1 - 31.12.XXXX-1.
    """

    if not isinstance(date, datetime):
        raise ValueError("The 'date' argument must be a valid datetime object.")

    log.debug("get_dates_range_before_date(): the date [%s].", date)

    tstamp_from: int = 0
    tstamp_to: int = 0

    # - processing and calculating dates
    if date.day == 1:  # today - 1st day of month, we need report for the previous month

        if date.month == 1:  # we are at 01.01.XXXX - we need report for Dec.XXXX - 1
            date_from = datetime(date.year - 1, 12, 1, tzinfo=tzinfo)  # from: 01 Dec Year-1 (prev. year)
            date_to = datetime(date.year - 1, 12, 31, tzinfo=tzinfo)  # to: 31 Dec Year-1 (prev. year)

        else:  # we are at 01.XX.XXXX - we need report for previous month
            date_from = datetime(date.year, date.month - 1, 1, tzinfo=tzinfo)  # from: 01 Month-1 Year
            _, last_day = calendar.monthrange(date.year, date.month - 1)  # last day of the previous month
            date_to = datetime(date.year, date.month - 1, last_day, tzinfo=tzinfo)  # to: LastDay Month-1 Year

    else:  # today isn't the 1st, we need report from 1st till yesterday

        date_from = datetime(date.year, date.month, 1, tzinfo=tzinfo)  # from: 01 Month Year
        date_to = datetime(date.year, date.month, date.day - 1, tzinfo=tzinfo)  # to: Day-1 Month Year

    # - final date/time - date from: XX.XX.XX 00:00:00 - date to: XX.XX.XXXX 23:59:59
    datetime_from = date_from.replace(hour=0, minute=0, second=0, microsecond=0)
    datetime_to = date_to.replace(hour=23, minute=59, second=59, microsecond=0)
    # timestamps from datetime objects
    tstamp_from = int(datetime_from.timestamp())
    tstamp_to = int(datetime_to.timestamp())

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
