"""DataUpdateCoordinator for Divoom Pixoo64 integration."""
from __future__ import annotations

import asyncio
import logging
import time
from datetime import timedelta
from typing import Any, Dict

from aiopixooapi.pixoo64 import Pixoo64
from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import (
    DataUpdateCoordinator,
    UpdateFailed,
)

from .const import DEFAULT_NAME, DOMAIN, SCAN_INTERVAL, THROTTLE_INTERVAL

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
        self._throttle_lock = asyncio.Lock()
        self._last_call = 0.0

    async def _throttled_api_call(self, coro):
        """Throttle API calls to avoid hitting the device too frequently."""
        async with self._throttle_lock:
            now = time.monotonic()
            elapsed = now - self._last_call
            if elapsed < THROTTLE_INTERVAL:
                await asyncio.sleep(THROTTLE_INTERVAL - elapsed)
            result = await coro
            self._last_call = time.monotonic()
            return result

    async def _async_update_data(self) -> Dict[str, Any]:
        """Update data via library."""
        try:
            # Throttle the API call
            settings = await self._throttled_api_call(self.api.get_all_settings())
            return {
                "is_on": int(settings["LightSwitch"]) == 1,
                "brightness": int(settings["Brightness"]),
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
            await self._throttled_api_call(self.api.set_brightness(brightness))
            await self.async_refresh()
        except Exception as err:
            self.logger.error("Failed to set brightness: %s", err)
            raise UpdateFailed(f"Failed to set brightness: {err}") from err

    async def async_close(self) -> None:
        """Close the API session."""
        await self.api.close()
