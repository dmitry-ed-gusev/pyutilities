# -*- coding: utf-8 -*-

"""
Useful date/time utilities and functions.

Created:  Dmitrii Gusev, 22.03.2026
Modified: Dmitrii Gusev, 10.05.2026
"""

from datetime import datetime, timedelta, timezone

import pendulum
from pendulum import Date

from pyutilities.defaults import MSG_MODULE_ISNT_RUNNABLE

MSK_TIMEZONE: timezone = timezone(timedelta(hours=3), name="Moscow Timezone (Russia)")
MSK_TIMEZONE_NAME: str = "Europe/Moscow"


def get_timestamp(
    current_timezone: timezone = MSK_TIMEZONE,
    days: float = 0,
    hours: float = 0,
    minutes: float = 0,
    seconds: float = 0,
) -> datetime:
    """Return timestamp: now (in the default timezone) +/- the specified time delta in hours / minutes /
    seconds. Default timezone can be changed by the function argument."""

    return datetime.now(current_timezone) + timedelta(
        days=days, hours=hours, minutes=minutes, seconds=seconds
    )


def get_dates_range_before_date(date: datetime) -> tuple[int, int]:
    """Generates two dates range - date_from/date_to for the time period 'before today' - from the 1st day
    of the current month till the today - 1 day (current month). In case today is 1st day - range for the
    whole previous month, if today is 01.01.XXXX - range for 01.12.XXXX-1 - 31.12.XXXX-1.
    """

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
    tstamp_from = pendulum.datetime(date_from.year, date_from.month, date_from.day)
    tstamp_to = pendulum.datetime(date_to.year, date_to.month, date_to.day)

    # - return the tuple of values
    return (tstamp_from.int_timestamp, tstamp_to.int_timestamp)


if __name__ == "__main__":
    print(MSG_MODULE_ISNT_RUNNABLE)
