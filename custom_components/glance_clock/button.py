"""Button platform for safe Glance Clock commands."""

from homeassistant.components.button import ButtonEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import EntityCategory
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import DOMAIN
from .entity import GlanceClockEntity
from .services.commands import send_safe_command


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up Glance Clock command buttons."""
    data = hass.data[DOMAIN][config_entry.entry_id]
    args = (
        config_entry,
        data["mac_address"],
        data["name"],
        data["connection_manager"],
    )
    async_add_entities(
        [
            GlanceClockCommandButton(
                *args, "Stop Timer", "stop_timer", "mdi:timer-stop"
            ),
            GlanceClockCommandButton(
                *args, "Stop Alarm", "stop_alarm", "mdi:alarm-off"
            ),
            GlanceClockCommandButton(
                *args, "Stop Scenes", "stop_scenes", "mdi:stop-circle-outline"
            ),
            GlanceClockCommandButton(
                *args, "Start Scenes", "start_scenes", "mdi:play-circle-outline"
            ),
        ]
    )


class GlanceClockCommandButton(GlanceClockEntity, ButtonEntity):
    """Run one allow-listed command on the clock."""

    _attr_entity_category = EntityCategory.CONFIG

    def __init__(
        self,
        config_entry,
        mac_address,
        device_name,
        connection_manager,
        label,
        command,
        icon,
    ):
        super().__init__(config_entry, mac_address, device_name, connection_manager)
        self._attr_name = f"{device_name} {label}"
        self._attr_unique_id = f"{mac_address}_{command}"
        self._attr_icon = icon
        self._command = command

    @property
    def available(self) -> bool:
        return self._connection_manager.is_connected

    async def async_press(self) -> None:
        await send_safe_command(self.hass, self._config_entry, self._command)
