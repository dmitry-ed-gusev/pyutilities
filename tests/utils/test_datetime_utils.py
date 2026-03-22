# -*- coding: utf-8 -*-

from datetime import datetime

from pyutilities.utils.datetime_utils import MSK_TIMEZONE, get_timestamp


def test_get_timestamp():

    assert datetime.now(MSK_TIMEZONE) > get_timestamp(hours=-10)
    assert datetime.now(MSK_TIMEZONE) > get_timestamp(minutes=-25)
    assert datetime.now(MSK_TIMEZONE) > get_timestamp(seconds=-45)

    assert datetime.now(MSK_TIMEZONE) < get_timestamp(hours=+1)
    assert datetime.now(MSK_TIMEZONE) < get_timestamp(minutes=+30)
    assert datetime.now(MSK_TIMEZONE) < get_timestamp(seconds=+300)
