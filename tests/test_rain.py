"""Tests for rain ForecastScene value encoding."""

from custom_components.glance_clock.rain import RAIN_TEMPLATE, encode_rain_values


def test_encodes_tenths_of_a_millimetre_and_pads() -> None:
    values, encoded, maximum = encode_rain_values(
        [{"precipitation": 0}, {"precipitation": 0.2}, {"precipitation": 0.9}]
    )

    assert values[:4] == [0, 2, 9, 0]
    assert len(values) == 24
    assert len(encoded) == 48
    assert encoded[:8] == bytes.fromhex("0000020009000000")
    assert maximum == 20


def test_clamps_heavy_and_invalid_precipitation() -> None:
    values, _, maximum = encode_rain_values(
        [{"precipitation": 4.2}, {"precipitation": -1}, {"precipitation": None}],
        max_mm_per_hour=2,
    )

    assert values[:3] == [20, 0, 0]
    assert maximum == 20


def test_uses_hypfer_umbrella_icon() -> None:
    assert RAIN_TEMPLATE == bytes([0xC2, 149]) + b" RAIN"
