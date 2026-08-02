"""Tests for settings protobuf conversion and cache-safe merging."""

from custom_components.glance_clock.glance_pb2 import Settings
from custom_components.glance_clock.settings import (
    DEFAULT_SETTINGS,
    merge_settings,
    settings_from_dict,
    settings_to_dict,
)


def test_round_trip_includes_all_known_settings() -> None:
    values = merge_settings(
        DEFAULT_SETTINGS,
        {
            "permanentMute": True,
            "permanentDND": True,
            "mgrSilentIntervalMin": 12,
            "mgrSilentIntervalMax": 34,
            "mgrUserActivityTimeout": 900,
            "dnd": {"recurring": True, "fromHour": 22, "tillHour": 7},
            "silent": {"recurring": True, "fromHour": 23, "tillHour": 6},
        },
    )

    encoded = settings_from_dict(values).SerializeToString()
    decoded = Settings()
    decoded.ParseFromString(encoded)

    assert settings_to_dict(decoded) == values


def test_partial_nested_update_preserves_schedule_siblings() -> None:
    current = merge_settings(
        DEFAULT_SETTINGS,
        {
            "dnd": {"recurring": False, "fromHour": 21, "tillHour": 8},
        },
    )

    updated = merge_settings(current, {"dnd": {"recurring": True}})

    assert updated["dnd"] == {
        "recurring": True,
        "fromHour": 21,
        "tillHour": 8,
    }


def test_merge_does_not_mutate_defaults_or_current_settings() -> None:
    current = merge_settings(DEFAULT_SETTINGS, {})

    updated = merge_settings(current, {"silent": {"fromHour": 20}})

    assert updated["silent"]["fromHour"] == 20
    assert current["silent"]["fromHour"] == 0
    assert DEFAULT_SETTINGS["silent"]["fromHour"] == 0
