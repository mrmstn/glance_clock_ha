"""Rain-forecast encoding helpers."""

import struct

RAIN_UNITS_PER_MM = 10
RAIN_TEMPLATE = bytes([0xC2, 149]) + b" RAIN"


def encode_rain_values(
    forecast: list[dict], max_mm_per_hour: float = 2.0
) -> tuple[list[int], bytes, int]:
    """Encode 24 precipitation values in tenths of a millimetre."""
    max_units = max(1, round(float(max_mm_per_hour) * RAIN_UNITS_PER_MM))
    values = []
    for hour in forecast[:24]:
        try:
            precipitation = max(0.0, float(hour.get("precipitation", 0.0)))
        except (TypeError, ValueError):
            precipitation = 0.0
        values.append(min(max_units, round(precipitation * RAIN_UNITS_PER_MM)))

    while len(values) < 24:
        values.append(0)

    encoded = b"".join(struct.pack("<h", value) for value in values)
    return values, encoded, max_units
