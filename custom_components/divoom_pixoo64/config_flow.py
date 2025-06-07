"""Config flow for the Divoom Pixoo64 integration."""

import aiopixooapi

from homeassistant.core import HomeAssistant
from homeassistant.helpers import config_entry_flow

from .const import DOMAIN


async def _async_has_devices(hass: HomeAssistant) -> bool:
    """Return if there are devices that can be discovered."""
    # TODO Check if there are any devices that can be discovered in the network.
    # devices = await hass.async_add_executor_job(aiopixooapi.divoom.Divoom.get_local_device_list)
    # return len(devices) > 0


config_entry_flow.register_discovery_flow(DOMAIN, "Divoom Pixoo64", _async_has_devices)
