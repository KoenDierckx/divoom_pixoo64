"""Config flow for the Divoom Pixoo64 integration."""

import logging
from typing import Any, Dict, cast

import voluptuous as vol
from aiopixooapi import PixooError
from aiopixooapi.pixoo64 import Pixoo64
from homeassistant import config_entries
from homeassistant.const import CONF_NAME
from homeassistant.data_entry_flow import FlowResult

from .const import CONF_HOST, DEFAULT_NAME, DOMAIN

_LOGGER = logging.getLogger(__name__)


class ConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Divoom Pixoo64."""

    VERSION = 1

    async def async_step_user(self, user_input=None) -> FlowResult:
        """Handle the initial step."""
        errors = {}
        
        if user_input is not None:
            # Test connection to the device
            pixoo64 = Pixoo64(user_input[CONF_HOST])
            try:
                # Directly await the coroutine
                await pixoo64.get_all_settings()

                # Create entry
                return cast(FlowResult, self.async_create_entry(
                    title=user_input.get(CONF_NAME, DEFAULT_NAME),
                    data=user_input,
                ))
            except PixooError:
                _LOGGER.exception("Unexpected exception")
                errors["base"] = "cannot_connect"
            finally:
                await pixoo64.close()

        return cast(FlowResult, self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {
                    vol.Required(CONF_HOST): str,
                    vol.Optional(CONF_NAME, default=DEFAULT_NAME): str,
                }
            ),
            errors=errors,
        ))

    async def async_step_discovery(self, discovery_info: Dict[str, Any]) -> FlowResult:
        """Handle discovery flow."""
        host = discovery_info.get("host")
        
        # Check if already configured
        await self.async_set_unique_id(host)
        self._abort_if_unique_id_configured()
        
        # Create entry
        return cast(FlowResult, self.async_create_entry(
            title=DEFAULT_NAME,
            data={
                CONF_HOST: host,
                CONF_NAME: DEFAULT_NAME,
            },
        ))
