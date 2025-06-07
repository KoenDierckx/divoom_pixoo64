"""DataUpdateCoordinator for Divoom Pixoo64 integration."""
from __future__ import annotations

import logging
from datetime import timedelta
from typing import Any, Dict

from aiopixooapi.pixoo64 import Pixoo64

from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import (
    DataUpdateCoordinator,
    UpdateFailed,
)

from .const import DEFAULT_NAME, DOMAIN, SCAN_INTERVAL

_LOGGER = logging.getLogger(__name__)


class DivoomPixooCoordinator(DataUpdateCoordinator[Dict[str, Any]]):
    """Class to manage fetching Divoom Pixoo data."""

    def __init__(
        self,
        hass: HomeAssistant,
        host: str,
        name: str,
        entry_id: str,
    ) -> None:
        """Initialize the coordinator."""
        super().__init__(
            hass,
            _LOGGER,
            name=f"{name} Coordinator",
            update_interval=timedelta(seconds=SCAN_INTERVAL),
        )
        self.host = host
        self.api = Pixoo64(host)
        self.entry_id = entry_id
        self._device_info = {
            "identifiers": {(DOMAIN, entry_id)},
            "name": name or DEFAULT_NAME,
            "manufacturer": "Divoom",
            "model": "Pixoo64",
        }

    async def _async_update_data(self) -> Dict[str, Any]:
        """Update data via library."""
        try:
            # Get device brightness - directly await the coroutine
            settings = await self.api.get_all_settings()
            
            return {
                "is_on": int(settings['LightSwitch']) == 1,
                "brightness": int(settings['Brightness']),
                "connected": True,
            }
        except Exception as err:
            # If we can't connect, assume the device is disconnected
            self.logger.error("Error communicating with Divoom Pixoo64: %s", err)
            return {
                "is_on": False,
                "brightness": 0,
                "connected": False,
            }
    
    @property
    def device_info(self) -> Dict[str, Any]:
        """Return device info."""
        return self._device_info
    
    async def async_set_brightness(self, brightness: int) -> None:
        """Set the brightness of the device."""
        try:
            # Directly await the coroutine
            await self.api.set_brightness(brightness)
            await self.async_refresh()
        except Exception as err:
            self.logger.error("Failed to set brightness: %s", err)
            raise UpdateFailed(f"Failed to set brightness: {err}") from err
