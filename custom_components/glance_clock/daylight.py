"""Daylight clock-face encoding helpers."""

import datetime
import struct

DAYLIGHT_TEMPLATE = bytes([0xC2, 133]) + b" DAY"
DAYLIGHT_MAX = 100


def encode_daylight_values(
    start: datetime.datetime,
    sun_events: dict[
        datetime.date, tuple[datetime.datetime | None, datetime.datetime | None]
    ],
) -> tuple[list[int], bytes]:
    """Encode whether the midpoint of each of the next 24 hours is daylight."""
    if start.tzinfo is None:
        raise ValueError("Daylight forecast start must be timezone-aware")

    values: list[int] = []
    for offset in range(24):
        midpoint = start + datetime.timedelta(hours=offset, minutes=30)
        sunrise, sunset = sun_events.get(midpoint.date(), (None, None))
        is_daylight = sunrise is not None and sunset is not None
        if is_daylight:
            sunrise = sunrise.astimezone(start.tzinfo)
            sunset = sunset.astimezone(start.tzinfo)
            is_daylight = sunrise <= midpoint < sunset
        values.append(DAYLIGHT_MAX if is_daylight else 0)

    encoded = b"".join(struct.pack("<h", value) for value in values)
    return values, encoded
