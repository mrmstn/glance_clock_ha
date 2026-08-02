"""Small helpers for the reverse-engineered Glance BLE protocol."""


def build_basic_command(command: int) -> bytes:
    """Build the official app's four-byte command envelope."""
    if not 0 <= command <= 0xFF:
        raise ValueError("command must fit in one unsigned byte")
    return bytes([command, 0, 0, 0])
