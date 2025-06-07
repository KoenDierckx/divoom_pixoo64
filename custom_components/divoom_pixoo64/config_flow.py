"""Config flow for the Divoom Pixoo64 integration."""

import logging
from typing import Any, Dict

import aiopixooapi
from aiopixooapi.divoom import Divoom
from aiopixooapi.pixoo64 import Pixoo64
import voluptuous as vol

from homeassistant import config_entries
from homeassistant.const import CONF_NAME
from homeassistant.core import HomeAssistant
from homeassistant.data_entry_flow import FlowResult
from homeassistant.exceptions import HomeAssistantError
import homeassistant.helpers.config_validation as cv

from .const import CONF_HOST, DEFAULT_NAME, DOMAIN

_LOGGER = logging.getLogger(__name__)


async def _async_has_devices(hass: HomeAssistant) -> bool:
    """Return if there are devices that can be discovered."""
    try:
        devices = await hass.async_add_executor_job(Divoom.get_local_device_list)
        return len(devices) > 0
    except Exception as exc:  # pylint: disable=broad-except
        _LOGGER.error("Error discovering Divoom devices: %s", exc)
        return False


class ConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Divoom Pixoo64."""

    VERSION = 1

    async def async_step_user(self, user_input=None) -> FlowResult:
        """Handle the initial step."""
        errors = {}
        
        if user_input is not None:
            try:
                # Test connection to the device
                pixoo = Pixoo64(user_input[CONF_HOST])
                # Directly await the coroutine
                await pixoo.get_all_settings()
                
                # Create entry
                return self.async_create_entry(
                    title=user_input.get(CONF_NAME, DEFAULT_NAME),
                    data=user_input,
                )
            except Exception:  # pylint: disable=broad-except
                _LOGGER.exception("Unexpected exception")
                errors["base"] = "cannot_connect"

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {
                    vol.Required(CONF_HOST): str,
                    vol.Optional(CONF_NAME, default=DEFAULT_NAME): str,
                }
            ),
            errors=errors,
        )

    async def async_step_discovery(self, discovery_info: Dict[str, Any]) -> FlowResult:
        """Handle discovery flow."""
        host = discovery_info.get("host")
        
        # Check if already configured
        await self.async_set_unique_id(host)
        self._abort_if_unique_id_configured()
        
        # Create entry
        return self.async_create_entry(
            title=DEFAULT_NAME,
            data={
                CONF_HOST: host,
                CONF_NAME: DEFAULT_NAME,
            },
        )
