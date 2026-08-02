"""Number controls for Glance Clock settings."""

from __future__ import annotations

from homeassistant.components.number import NumberEntity, NumberMode
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import EntityCategory, UnitOfTime
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import DOMAIN
from .entity import GlanceClockEntity


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up Glance Clock number entities."""
    data = hass.data[DOMAIN][config_entry.entry_id]
    args = (
        config_entry,
        data["mac_address"],
        data["name"],
        data["connection_manager"],
    )
    async_add_entities(
        [
            GlanceClockSettingsNumber(
                *args,
                "Activity Timeout",
                "activity_timeout",
                "mgrUserActivityTimeout",
                0,
                3600,
                10,
                "mdi:timer-outline",
                UnitOfTime.SECONDS,
            ),
            GlanceClockSettingsNumber(
                *args,
                "DND From Hour",
                "dnd_from_hour",
                ("dnd", "fromHour"),
                0,
                23,
                1,
                "mdi:clock-start",
            ),
            GlanceClockSettingsNumber(
                *args,
                "DND Until Hour",
                "dnd_until_hour",
                ("dnd", "tillHour"),
                0,
                23,
                1,
                "mdi:clock-end",
            ),
            GlanceClockSettingsNumber(
                *args,
                "Silent From Hour",
                "silent_from_hour",
                ("silent", "fromHour"),
                0,
                23,
                1,
                "mdi:clock-start",
            ),
            GlanceClockSettingsNumber(
                *args,
                "Silent Until Hour",
                "silent_until_hour",
                ("silent", "tillHour"),
                0,
                23,
                1,
                "mdi:clock-end",
            ),
        ]
    )


class GlanceClockSettingsNumber(GlanceClockEntity, NumberEntity):
    """An integer Glance setting exposed as a number."""

    _attr_entity_category = EntityCategory.CONFIG
    _attr_mode = NumberMode.BOX

    def __init__(
        self,
        config_entry,
        mac_address,
        device_name,
        connection_manager,
        label,
        unique_suffix,
        setting,
        minimum,
        maximum,
        step,
        icon,
        unit=None,
    ):
        super().__init__(config_entry, mac_address, device_name, connection_manager)
        self._attr_name = f"{device_name} {label}"
        self._attr_unique_id = f"{mac_address}_{unique_suffix}"
        self._attr_icon = icon
        self._attr_native_min_value = minimum
        self._attr_native_max_value = maximum
        self._attr_native_step = step
        self._attr_native_unit_of_measurement = unit
        self._setting = setting
        self._value = None
        self._available = False

    @property
    def native_value(self) -> float | None:
        return self._value

    @property
    def available(self) -> bool:
        return self._available and self._connection_manager.is_connected

    def _value_from(self, settings):
        if isinstance(self._setting, tuple):
            return settings.get(self._setting[0], {}).get(self._setting[1])
        return settings.get(self._setting)

    def _change(self, value):
        if isinstance(self._setting, tuple):
            return {self._setting[0]: {self._setting[1]: value}}
        return {self._setting: value}

    async def async_set_native_value(self, value: float) -> None:
        int_value = int(value)
        if await self._write_settings(self._change(int_value)):
            self._value = int_value
            self.async_write_ha_state()

    async def async_added_to_hass(self) -> None:
        await super().async_added_to_hass()
        self._connection_manager.add_connection_callback(
            self._on_connection_established
        )
        await self.async_update()

    async def _on_connection_established(self) -> None:
        await self.async_update()
        self.async_write_ha_state()

    async def async_update(self) -> None:
        settings = await self._read_settings()
        if settings is not None:
            value = self._value_from(settings)
            if value is not None:
                self._value = int(value)
                self._available = True
                return
        self._available = self._connection_manager.is_connected

    async def async_will_remove_from_hass(self) -> None:
        self._connection_manager.remove_connection_callback(
            self._on_connection_established
        )
        await super().async_will_remove_from_hass()
