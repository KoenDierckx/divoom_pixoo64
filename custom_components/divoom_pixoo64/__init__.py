"""The Divoom Pixoo64 integration."""

from __future__ import annotations

import logging
from typing import TypeVar

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_HOST, CONF_NAME, Platform
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import ConfigEntryNotReady

from .const import DEFAULT_NAME, DOMAIN
from .coordinator import DivoomPixooCoordinator

_LOGGER = logging.getLogger(__name__)

# Supported platforms
PLATFORMS: list[Platform] = [
    Platform.LIGHT,
]

T = TypeVar("T")


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up Divoom Pixoo64 from a config entry."""
    host = entry.data[CONF_HOST]
    name = entry.data.get(CONF_NAME, DEFAULT_NAME)

    try:
        # Create coordinator with the host parameter
        coordinator = DivoomPixooCoordinator(
            hass=hass,
            host=host,
            name=name,
            entry_id=entry.entry_id,
        )

        # Fetch initial data
        await coordinator.async_config_entry_first_refresh()
        
        # Store coordinator for platforms to access
        hass.data.setdefault(DOMAIN, {})
        hass.data[DOMAIN][entry.entry_id] = coordinator
        
        # Set up all platforms
        await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
        
        return True
        
    except Exception as ex:
        _LOGGER.error("Failed to connect to Divoom Pixoo64 at %s: %s", host, ex)
        raise ConfigEntryNotReady(f"Failed to connect to Divoom Pixoo64 at {host}") from ex


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    if unload_ok := await hass.config_entries.async_unload_platforms(entry, PLATFORMS):
        hass.data[DOMAIN].pop(entry.entry_id)
    
    return unload_ok