"""Glance Clock settings serialization helpers."""

from __future__ import annotations

from copy import deepcopy
from typing import Any

from .glance_pb2 import Settings  # type: ignore


DEFAULT_SETTINGS: dict[str, Any] = {
    "dnd": {"recurring": False, "fromHour": 0, "tillHour": 0},
    "nightModeEnabled": True,
    "permanentDND": False,
    "permanentMute": False,
    "dateFormat": 0,
    "mgrSilentIntervalMin": 0,
    "mgrSilentIntervalMax": 0,
    "pointsAlwaysEnabled": False,
    "displayBrightness": 0,
    "timeModeEnable": True,
    "timeFormat12": False,
    "mgrUserActivityTimeout": 600,
    "silent": {"recurring": False, "fromHour": 0, "tillHour": 0},
}


def merge_settings(
    base: dict[str, Any] | None, changes: dict[str, Any]
) -> dict[str, Any]:
    """Merge partial settings without dropping sibling fields in nested messages."""
    merged = deepcopy(DEFAULT_SETTINGS)
    for source in (base or {}, changes):
        for key, value in source.items():
            if key in ("dnd", "silent") and isinstance(value, dict):
                merged[key].update(value)
            else:
                merged[key] = value
    return merged


def settings_to_dict(settings: Settings) -> dict[str, Any]:
    """Convert the protobuf settings message into the integration representation."""
    return {
        "dnd": {
            "recurring": settings.dnd.recurring,
            "fromHour": settings.dnd.fromHour,
            "tillHour": settings.dnd.tillHour,
        },
        "nightModeEnabled": settings.nightModeEnabled,
        "permanentDND": settings.permanentDND,
        "permanentMute": settings.permanentMute,
        "dateFormat": settings.dateFormat,
        "mgrSilentIntervalMin": settings.mgrSilentIntervalMin,
        "mgrSilentIntervalMax": settings.mgrSilentIntervalMax,
        "pointsAlwaysEnabled": settings.pointsAlwaysEnabled,
        "displayBrightness": settings.displayBrightness,
        "timeModeEnable": settings.timeModeEnable,
        "timeFormat12": settings.timeFormat12,
        "mgrUserActivityTimeout": settings.mgrUserActivityTimeout,
        "silent": {
            "recurring": settings.silent.recurring,
            "fromHour": settings.silent.fromHour,
            "tillHour": settings.silent.tillHour,
        },
    }


def settings_from_dict(values: dict[str, Any]) -> Settings:
    """Create a complete protobuf settings message from a settings dictionary."""
    values = merge_settings(None, values)
    settings = Settings()
    settings.dnd.recurring = bool(values["dnd"]["recurring"])
    settings.dnd.fromHour = int(values["dnd"]["fromHour"])
    settings.dnd.tillHour = int(values["dnd"]["tillHour"])
    settings.nightModeEnabled = bool(values["nightModeEnabled"])
    settings.permanentDND = bool(values["permanentDND"])
    settings.permanentMute = bool(values["permanentMute"])
    settings.dateFormat = int(values["dateFormat"])
    settings.mgrSilentIntervalMin = int(values["mgrSilentIntervalMin"])
    settings.mgrSilentIntervalMax = int(values["mgrSilentIntervalMax"])
    settings.pointsAlwaysEnabled = bool(values["pointsAlwaysEnabled"])
    settings.displayBrightness = int(values["displayBrightness"])
    settings.timeModeEnable = bool(values["timeModeEnable"])
    settings.timeFormat12 = bool(values["timeFormat12"])
    settings.mgrUserActivityTimeout = int(values["mgrUserActivityTimeout"])
    settings.silent.recurring = bool(values["silent"]["recurring"])
    settings.silent.fromHour = int(values["silent"]["fromHour"])
    settings.silent.tillHour = int(values["silent"]["tillHour"])
    return settings
