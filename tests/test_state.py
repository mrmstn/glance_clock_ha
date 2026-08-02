"""Tests for the Glance Clock State characteristic decoder."""

import pytest

from custom_components.glance_clock.state import ClockState


def test_decode_live_state_sample() -> None:
    state = ClockState.from_bytes(bytes.fromhex("04 22"))

    assert state.word == 0x2204
    assert state.power_saving_mode == 0
    assert state.unknown_bits == 0
    assert state.as_attributes()["scenes_enabled"] is True
    assert state.as_attributes()["cable_connected"] is True
    assert state.as_attributes()["no_data"] is True
    assert state.as_attributes()["charging"] is False


def test_decode_pads_one_byte_like_official_app() -> None:
    state = ClockState.from_bytes(b"\x0b")

    assert state.word == 0x000B
    assert state.power_saving_mode == 3
    assert state.as_attributes()["power_saving_high_threshold"] == 10
    assert state.as_attributes()["power_saving_low_threshold"] == 0
    assert state.as_attributes()["muted"] is True


def test_preserves_undocumented_high_bits() -> None:
    state = ClockState.from_bytes(bytes.fromhex("08 b2"))

    assert state.word == 0xB208
    assert state.unknown_bits == 0x8000
    assert state.as_attributes()["unknown_bits"] == "0x8000"


def test_rejects_empty_value() -> None:
    with pytest.raises(ValueError, match="no data"):
        ClockState.from_bytes(b"")
