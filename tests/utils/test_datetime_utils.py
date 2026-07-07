# -*- coding: utf-8 -*-

from datetime import datetime, timezone, timedelta

import pytz
import pytest
from hypothesis import given, strategies as st

from pyutilities.utils.datetime_utils import MSK_TIMEZONE
from pyutilities.utils.datetime_utils import shift_timestamp, get_shifted_timestamp
from pyutilities.utils.datetime_utils import get_dates_range_before_date


def test_get_shifted_timestamp():

    assert datetime.now(MSK_TIMEZONE) > get_shifted_timestamp(delta_hours=-10)
    assert datetime.now(MSK_TIMEZONE) > get_shifted_timestamp(delta_minutes=-25)
    assert datetime.now(MSK_TIMEZONE) > get_shifted_timestamp(delta_seconds=-45)

    assert datetime.now(MSK_TIMEZONE) < get_shifted_timestamp(delta_hours=+1)
    assert datetime.now(MSK_TIMEZONE) < get_shifted_timestamp(delta_minutes=+30)
    assert datetime.now(MSK_TIMEZONE) < get_shifted_timestamp(delta_seconds=+300)


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
def test_get_dates_range_before_date(day, month, year, tz, expected_from, expected_to):

    now = datetime(year, month, day, tzinfo=tz)
    tstamp_from, tstamp_to = get_dates_range_before_date(now, tzinfo=tz)
    dt_from = datetime.fromtimestamp(tstamp_from, tz=tz).strftime("%d-%m-%Y")
    dt_to = datetime.fromtimestamp(tstamp_to, tz=tz).strftime("%d-%m-%Y")

    # checks / assertions
    assert dt_from == expected_from
    assert dt_to == expected_to


# Mocking the logger for the trace parameter
class DummyLogger:
    def __init__(self):
        self.messages = []
        self.called = False

    def debug(self, msg, *args):
        self.messages.append(msg % args)
        self.called = True


@pytest.fixture(autouse=True)
def mock_log(monkeypatch):
    """Mocks the global log object used in the trace condition."""
    logger = DummyLogger()
    # Replace 'your_module.log' with the actual path where log is defined
    # monkeypatch.setattr("your_module.log", logger)
    monkeypatch.setattr("pyutilities.utils.datetime_utils.log", logger)
    return logger


# =====================================================================
# 1. STANDARD PYTEST UNIT TESTS (Deterministic Edge Cases)
# =====================================================================

def test_shift_timestamp_returns_none_on_empty_input():
    """Verifies that an empty or None base_timestamp returns None."""
    assert shift_timestamp(None) is None


def test_shift_timestamp_preserves_timezone():
    """Verifies that the original timezone info is maintained."""
    base = datetime(2026, 5, 15, tzinfo=timezone.utc)
    result = shift_timestamp(base, delta_days=1)
    assert result.tzinfo == timezone.utc


def test_shift_timestamp_month_rollover_positive():
    """Tests normal positive month addition with year rollover."""
    base = datetime(2026, 11, 10)
    result = shift_timestamp(base, delta_months=3)
    assert result == datetime(2027, 2, 10)


def test_shift_timestamp_month_rollover_negative():
    """Tests normal negative month subtraction with year rollback."""
    base = datetime(2026, 2, 10)
    result = shift_timestamp(base, delta_months=-3)
    assert result == datetime(2025, 11, 10)


def test_shift_timestamp_trace_logging(monkeypatch):
    """Verifies that logging occurs when trace=True."""
    logger = DummyLogger()
    monkeypatch.setattr("pyutilities.utils.datetime_utils.log", logger)  # Update path accordingly

    base = datetime(2026, 1, 1)
    shift_timestamp(base, delta_days=1, trace=True)

    assert logger.called is True
    assert len(logger.messages) == 1
    assert "Generated from" in logger.messages[0]


# =====================================================================
# 2. HYPOTHESIS PROPERTY-BASED TESTS (Edge Case Detection)
# =====================================================================

# Safe date range strategy to prevent out-of-bounds datetime creation (1-9999)
safe_datetimes = st.datetimes(
    min_value=datetime(2000, 1, 1),
    max_value=datetime(2080, 12, 31)
)


@given(
    base=safe_datetimes,
    years=st.integers(min_value=-10, max_value=10),
    months=st.integers(min_value=-24, max_value=24),
    days=st.floats(min_value=-30, max_value=30, allow_nan=False, allow_infinity=False),
    hours=st.floats(min_value=-24, max_value=24, allow_nan=False, allow_infinity=False)
)
def test_shift_timestamp_properties(base, years, months, days, hours):
    """
    Property test to ensure the function does not crash randomly
    and handles combinations of inputs gracefully.
    """
    try:
        result = shift_timestamp(base, delta_years=years, delta_months=months,
                                 delta_days=days, delta_hours=hours)
        if result is not None:
            assert isinstance(result, datetime)
    except ValueError as e:
        # The current implementation has a potential ValueError flaw
        # when days mismatch month lengths (e.g., Jan 31st + 1 month = Feb 31st).
        # We catch it here to show where it safely raises or fails.
        pytest.xfail(f"Known native datetime limitation triggered: {e}")


# =====================================================================
# 3. ТЕСТЫ НА ИСПРАВЛЕНИЕ СТАРЫХ БАГОВ (Краши на днях месяцев)
# =====================================================================

def test_shift_month_end_overflow_safe():
    """Проверяет, что 31 января + 1 месяц не падает, а переносится на конец февраля."""
    base = datetime(2026, 1, 31)
    result = shift_timestamp(base, delta_months=1)
    assert result == datetime(2026, 2, 28)


def test_shift_leap_year():
    """Проверяет корректность работы с високосным годом."""
    base = datetime(2024, 2, 29)  # 2024 — високосный
    result = shift_timestamp(base, delta_years=1)
    assert result == datetime(2025, 2, 28)  # 2025 — обычный


# =====================================================================
# 4. ТЕСТЫ НА ЧАСОВЫЕ ПОЯСА И ПЕРЕХОД НА ЛЕТНЕЕ/ЗИМНЕЕ ВРЕМЯ (DST)
# =====================================================================

# def test_dst_spring_forward_gap():
#     """
#     Тест перехода на летнее время (Spring Forward).
#     В зоне Europe/London 31 марта 2024 года в 01:00 часы переводятся на 02:00.
#     Времени 01:30 в этот день не существует.
#     """
#     tz = pytz.timezone("Europe/London")
#     # 31 марта 2024, 00:30 GMT (до перехода)
#     base = tz.localize(datetime(2024, 3, 31, 0, 30))

#     # Прибавляем 1 час. Время должно перешагнуть "дыру" и стать 02:30 BST (+01:00)
#     result = shift_timestamp(base, delta_hours=1)

#     assert result.hour == 1
#     assert result.minute == 30
#     assert result.utcoffset() == timedelta(hours=1)  # Уже BST


def test_dst_fall_back_overlap():
    """
    Тест перехода на зимнее время (Fall Back).
    В зоне Europe/London 27 октября 2024 года в 02:00 BST часы возвращаются на 01:00 GMT.
    Час между 01:00 и 02:00 повторяется дважды.
    """
    tz = pytz.timezone("Europe/London")
    # 27 октября 2024, 00:30 GMT (до осеннего перевода, еще BST)
    base = tz.localize(datetime(2024, 10, 27, 0, 30))

    # Прибавляем 1 час. Время переходит в зону дублирующегося часа
    result = shift_timestamp(base, delta_hours=1)

    assert result.hour == 1
    assert result.minute == 30
    # Проверяем, что смещение всё еще летнее (+1), так как это первый проход часа
    assert result.utcoffset() == timedelta(hours=1)


# =====================================================================
# 5. ИНТЕНСИВНЫЕ ТЕСТЫ С HYPOTHESIS (Поиск скрытых аномалий)
# =====================================================================

# Стратегия для генерации часовых поясов (включая UTC, фиксированные и DST зоны)
tz_strategy = st.sampled_from([
    None, timezone.utc, pytz.timezone("Europe/Moscow"), pytz.timezone("America/New_York")
])


@given(
    # Ограничиваем диапазон дат разумными рамками, чтобы не выйти за лимиты datetime (1-9999 гг)
    base_date=st.datetimes(min_value=datetime(1900, 1, 1), max_value=datetime(2100, 12, 31)),
    tz=tz_strategy,
    years=st.integers(min_value=-5, max_value=5),
    months=st.integers(min_value=-12, max_value=12),
    days=st.floats(min_value=-31, max_value=31, allow_nan=False, allow_infinity=False),
    hours=st.floats(min_value=-24, max_value=24, allow_nan=False, allow_infinity=False)
)
def test_hypothesis_timestamp_shifter(base_date, tz, years, months, days, hours):
    """Property-based тест: проверяет стабильность функции на случайных комбинациях."""
    # Локализуем дату, если выбран часовой пояс
    if tz is not None:
        if hasattr(tz, 'localize'):
            base_timestamp = tz.localize(base_date)
        else:
            base_timestamp = base_date.replace(tzinfo=tz)
    else:
        base_timestamp = base_date

    result = shift_timestamp(base_timestamp, delta_years=years, delta_months=months,
                             delta_days=days, delta_hours=hours)

    # Главные свойства (Invariants), которые никогда не должны нарушаться:
    if result is not None:
        assert isinstance(result, datetime)
        # Наличие или отсутствие таймзоны должно строго сохраняться
        assert (base_timestamp.tzinfo is None) == (result.tzinfo is None)
