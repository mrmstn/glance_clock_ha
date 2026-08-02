"""Tests for factory demo IDs recovered from the official Android app."""

from custom_components.glance_clock.const import (
    FACTORY_DEMO_SCENES,
    FACTORY_DEMO_SCENES_REVERSE,
)


def test_firmware_1_6_7_smile_and_off_values() -> None:
    assert FACTORY_DEMO_SCENES["Off"] == 0
    assert FACTORY_DEMO_SCENES["Smile"] == 6


def test_every_factory_demo_value_round_trips() -> None:
    for name, value in FACTORY_DEMO_SCENES.items():
        assert FACTORY_DEMO_SCENES_REVERSE[value] == name


def test_repeat_all_uses_unsigned_byte_value() -> None:
    assert bytes([FACTORY_DEMO_SCENES["Repeat All"]]) == b"\xff"
