"""Decode the Glance Clock State characteristic."""

from __future__ import annotations

from dataclasses import dataclass


STATE_FLAGS = {
    "scenes_enabled": 0x0004,
    "muted": 0x0008,
    "do_not_disturb": 0x0010,
    "ancs_enabled": 0x0020,
    "homing_failure": 0x0040,
    "homing_in_progress": 0x0080,
    "time_adjustment_in_progress": 0x0100,
    "cable_connected": 0x0200,
    "homing_confirmation_wait": 0x0400,
    "motor_failure": 0x0800,
    "charging": 0x1000,
    "no_data": 0x2000,
}

POWER_SAVING_THRESHOLDS = {
    0: (100, 50),
    1: (50, 25),
    2: (25, 10),
    3: (10, 0),
}

KNOWN_MASK = 0x3FFF


@dataclass(frozen=True)
class ClockState:
    """Decoded little-endian State characteristic value."""

    word: int

    @classmethod
    def from_bytes(cls, data: bytes | bytearray) -> "ClockState":
        """Decode one or two bytes, matching the official application's parser."""
        if not data:
            raise ValueError("State characteristic returned no data")
        return cls(int.from_bytes(bytes(data[:2]).ljust(2, b"\x00"), "little"))

    @property
    def power_saving_mode(self) -> int:
        """Return power-saving mode 0 through 3."""
        return self.word & 0x0003

    @property
    def unknown_bits(self) -> int:
        """Return bits not interpreted by the official app."""
        return self.word & ~KNOWN_MASK & 0xFFFF

    def as_attributes(self) -> dict[str, bool | int | str]:
        """Return Home Assistant-friendly diagnostic attributes."""
        high, low = POWER_SAVING_THRESHOLDS[self.power_saving_mode]
        attributes: dict[str, bool | int | str] = {
            "raw_hex": f"0x{self.word:04x}",
            "power_saving_mode": self.power_saving_mode,
            "power_saving_high_threshold": high,
            "power_saving_low_threshold": low,
            "unknown_bits": f"0x{self.unknown_bits:04x}",
        }
        attributes.update(
            {name: bool(self.word & mask) for name, mask in STATE_FLAGS.items()}
        )
        return attributes
