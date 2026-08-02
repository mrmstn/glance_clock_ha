"""Safe command services for Glance Clock."""

import logging

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant, ServiceCall

from ..const import DOMAIN

_LOGGER = logging.getLogger(__name__)

SAFE_COMMANDS = {
    "stop_timer": 10,
    "stop_alarm": 20,
    "stop_scenes": 30,
    "start_scenes": 31,
}


async def send_safe_command(
    hass: HomeAssistant, entry: ConfigEntry, command_name: str
) -> bool:
    """Send one of the explicitly allow-listed non-destructive commands."""
    command = SAFE_COMMANDS[command_name]
    manager = hass.data[DOMAIN][entry.entry_id]["connection_manager"]
    success = await manager.send_command(bytes([command, 0, 0, 0]))
    if not success:
        _LOGGER.error("Failed to send Glance Clock command: %s", command_name)
    return success


async def handle_safe_command(
    hass: HomeAssistant,
    entry: ConfigEntry,
    call: ServiceCall,
) -> None:
    """Handle a service whose name maps to a safe command."""
    await send_safe_command(hass, entry, call.service)
