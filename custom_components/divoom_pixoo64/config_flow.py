"""Config flow for the Divoom Pixoo64 integration."""

import logging
from typing import Any, Dict

import voluptuous as vol
from aiopixooapi.divoom import Divoom
from aiopixooapi.pixoo64 import Pixoo64
from homeassistant import config_entries
from homeassistant.components.dhcp import DhcpServiceInfo
from homeassistant.const import CONF_MAC, CONF_NAME
from homeassistant.core import HomeAssistant
from homeassistant.data_entry_flow import FlowResult

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
    
    async def async_step_dhcp(self, discovery_info: DhcpServiceInfo) -> FlowResult:
        """Handle DHCP discovery."""
        _LOGGER.info("Discovered Pixoo device via DHCP: %s", discovery_info)
        
        # Use MAC address as the unique ID
        await self.async_set_unique_id(discovery_info.macaddress)
        self._abort_if_unique_id_configured(
            updates={CONF_HOST: discovery_info.ip}
        )
        
        # Use hostname as part of the name if available
        hostname = discovery_info.hostname
        name = f"Pixoo ({hostname})" if hostname else DEFAULT_NAME
        
        # Try to connect to device
        try:
            pixoo = Pixoo64(discovery_info.ip)
            await pixoo.get_all_settings()
            
            return self.async_create_entry(
                title=name,
                data={
                    CONF_HOST: discovery_info.ip,
                    CONF_NAME: name,
                    CONF_MAC: discovery_info.macaddress,
                },
            )
        except Exception as exc:  # pylint: disable=broad-except
            _LOGGER.error("Failed to connect to discovered Pixoo device: %s", exc)
            # Store discovery info for the confirm step
            self.context["dhcp_discovery"] = {
                CONF_HOST: discovery_info.ip,
                CONF_NAME: name,
                CONF_MAC: discovery_info.macaddress,
            }
            return await self.async_step_dhcp_confirm()
    
    async def async_step_dhcp_confirm(self, user_input=None) -> FlowResult:
        """Confirm DHCP discovery."""
        errors = {}
        discovery_info = self.context.get("dhcp_discovery", {})
        
        if user_input is not None:
            try:
                # Test connection to the device
                pixoo = Pixoo64(discovery_info[CONF_HOST])
                await pixoo.get_all_settings()
                
                # Create entry
                return self.async_create_entry(
                    title=discovery_info[CONF_NAME],
                    data=discovery_info,
                )
            except Exception:  # pylint: disable=broad-except
                _LOGGER.exception("Unexpected exception")
                errors["base"] = "cannot_connect"
        
        return self.async_show_form(
            step_id="dhcp_confirm",
            description_placeholders={
                "host": discovery_info.get(CONF_HOST),
                "name": discovery_info.get(CONF_NAME),
            },
            errors=errors,
        )
