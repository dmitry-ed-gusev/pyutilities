# -*- coding: utf-8 -*-

from datetime import datetime

import pytest

from pyutilities.utils.datetime_utils import MSK_TIMEZONE
from pyutilities.utils.datetime_utils import get_timestamp, get_dates_range_before_today


def test_get_timestamp():

    assert datetime.now(MSK_TIMEZONE) > get_timestamp(hours=-10)
    assert datetime.now(MSK_TIMEZONE) > get_timestamp(minutes=-25)
    assert datetime.now(MSK_TIMEZONE) > get_timestamp(seconds=-45)

    assert datetime.now(MSK_TIMEZONE) < get_timestamp(hours=+1)
    assert datetime.now(MSK_TIMEZONE) < get_timestamp(minutes=+30)
    assert datetime.now(MSK_TIMEZONE) < get_timestamp(seconds=+300)


@pytest.mark.parametrize("day, month, year, tz, expected_from, expected_to", [
    (2, 3, 2026, None, "01-03-2026", "01-03-2026"), (31, 12, 2025, None, "01-12-2025", "30-12-2025"),
    (1, 1, 2026, None, "01-12-2025", "31-12-2025"), (1, 3, 2020, None, "01-02-2020", "29-02-2020"),
    (10, 10, 2022, None, "01-10-2022", "09-10-2022"),

    (2, 3, 2026, MSK_TIMEZONE, "01-03-2026", "01-03-2026"),
    (31, 12, 2025, MSK_TIMEZONE, "01-12-2025", "30-12-2025"),
    (1, 1, 2026, MSK_TIMEZONE, "01-12-2025", "31-12-2025"),
    (1, 3, 2020, MSK_TIMEZONE, "01-02-2020", "29-02-2020"),
    (10, 10, 2022, MSK_TIMEZONE, "01-10-2022", "09-10-2022")

])
def test_get_dates_range_before_today(day, month, year, tz, expected_from, expected_to):

    now = datetime(year, month, day, tzinfo=tz)
    tstamp_from, tstamp_to = get_dates_range_before_today(now)
    dt_from = datetime.fromtimestamp(tstamp_from).strftime("%d-%m-%Y")
    dt_to = datetime.fromtimestamp(tstamp_to).strftime("%d-%m-%Y")

    # checks / assertions
    assert dt_from == expected_from
    assert dt_to == expected_to
