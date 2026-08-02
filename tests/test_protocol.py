"""Tests for common Glance BLE command encoding."""

import pytest

from custom_components.glance_clock.protocol import build_basic_command


@pytest.mark.parametrize("command", [10, 20, 30, 31, 35, 60, 61])
def test_build_basic_command(command: int) -> None:
    assert build_basic_command(command) == bytes([command, 0, 0, 0])


@pytest.mark.parametrize("command", [-1, 256])
def test_rejects_out_of_range_command(command: int) -> None:
    with pytest.raises(ValueError, match="unsigned byte"):
        build_basic_command(command)
