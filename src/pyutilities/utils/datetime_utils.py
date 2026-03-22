# -*- coding: utf-8 -*-

"""
Useful date/time utilities and functions.

Created:  Dmitrii Gusev, 22.03.2026
Modified: Dmitrii Gusev, 22.03.2026
"""

from datetime import datetime, timedelta, timezone

from pyutilities.defaults import MSG_MODULE_ISNT_RUNNABLE

MSK_TIMEZONE: timezone = timezone(timedelta(hours=3), name="Moscow Timezone (Russia)")


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


if __name__ == "__main__":
    print(MSG_MODULE_ISNT_RUNNABLE)
