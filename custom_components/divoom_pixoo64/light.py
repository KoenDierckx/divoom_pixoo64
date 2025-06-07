"""Light platform for Divoom Pixoo64 integration."""
from __future__ import annotations

import logging
from typing import Any

from homeassistant.components.light import (
    ATTR_BRIGHTNESS,
    ColorMode,
    LightEntity,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .coordinator import DivoomPixooCoordinator
from .const import DEFAULT_BRIGHTNESS, DOMAIN

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the Divoom Pixoo64 light platform."""
    coordinator = hass.data[DOMAIN][entry.entry_id]

    async_add_entities(
        [DivoomPixoo64Light(coordinator)],
    )


class DivoomPixoo64Light(CoordinatorEntity[DivoomPixooCoordinator], LightEntity):
    """Representation of a Divoom Pixoo64 light."""

    _attr_has_entity_name = True
    _attr_name = "Display"
    _attr_color_mode = ColorMode.BRIGHTNESS
    _attr_supported_color_modes = {ColorMode.BRIGHTNESS}

    def __init__(self, coordinator: DivoomPixooCoordinator) -> None:
        """Initialize the light entity."""
        super().__init__(coordinator)
        self._attr_unique_id = f"{coordinator.entry_id}_light"
        self._attr_device_info = coordinator.device_info

    @property
    def is_on(self) -> bool:
        """Return true if the light is on."""
        return self.coordinator.data.get("is_on", False)

    @property
    def brightness(self) -> int:
        """Return the brightness of the light."""
        # Convert 0-100 to 0-255
        brightness_pct = self.coordinator.data.get("brightness", 0)
        return int(brightness_pct * 255 / 100)

    @property
    def available(self) -> bool:
        """Return True if entity is available."""
        return self.coordinator.data.get("connected", False)

    async def async_turn_on(self, **kwargs: Any) -> None:
        """Turn on the light."""
        if ATTR_BRIGHTNESS in kwargs:
            # Convert 0-255 to 0-100
            brightness_pct = int(kwargs[ATTR_BRIGHTNESS] * 100 / 255)
            await self.coordinator.async_set_brightness(brightness_pct)
        else:
            await self.coordinator.async_set_brightness(DEFAULT_BRIGHTNESS)

    async def async_turn_off(self, **kwargs: Any) -> None:
        """Turn off the light."""
        await self.coordinator.async_set_brightness(0)
