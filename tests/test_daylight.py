"""Tests for daylight ForecastScene value encoding."""

import datetime

import pytest

from custom_components.glance_clock.daylight import encode_daylight_values


def test_encodes_daylight_at_hour_midpoints_across_two_dates() -> None:
    timezone = datetime.timezone(datetime.timedelta(hours=2))
    start = datetime.datetime(2026, 8, 3, 19, tzinfo=timezone)
    events = {
        datetime.date(2026, 8, 3): (
            datetime.datetime(2026, 8, 3, 6, tzinfo=timezone),
            datetime.datetime(2026, 8, 3, 21, tzinfo=timezone),
        ),
        datetime.date(2026, 8, 4): (
            datetime.datetime(2026, 8, 4, 6, tzinfo=timezone),
            datetime.datetime(2026, 8, 4, 21, tzinfo=timezone),
        ),
    }

    values, encoded = encode_daylight_values(start, events)

    assert values[:3] == [100, 100, 0]
    assert values[10:12] == [0, 100]
    assert values[23] == 100
    assert len(values) == 24
    assert len(encoded) == 48


def test_requires_timezone_aware_start() -> None:
    with pytest.raises(ValueError, match="timezone-aware"):
        encode_daylight_values(datetime.datetime(2026, 8, 3, 5), {})
