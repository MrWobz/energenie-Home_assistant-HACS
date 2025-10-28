"""Energenie ENER314-RT Light platform."""
import asyncio
import logging

from homeassistant.components.light import LightEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import (
    DOMAIN,
    DEVICE_TYPE_LIGHT,
    CONF_DEVICE_1_NAME,
    CONF_DEVICE_1_TYPE,
    CONF_DEVICE_2_NAME,
    CONF_DEVICE_2_TYPE,
    CONF_DEVICE_3_NAME,
    CONF_DEVICE_3_TYPE,
    CONF_DEVICE_4_NAME,
    CONF_DEVICE_4_TYPE,
)

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up Energenie lights from a config entry."""
    lights = []
    
    # Only create lights for enabled devices of light type
    if config_entry.data.get("device_1_enabled", True) and config_entry.data.get(CONF_DEVICE_1_TYPE) == DEVICE_TYPE_LIGHT:
        lights.append(EnergenieLight(1, config_entry.data.get(CONF_DEVICE_1_NAME), config_entry.entry_id))
    
    if config_entry.data.get("device_2_enabled", False) and config_entry.data.get(CONF_DEVICE_2_TYPE) == DEVICE_TYPE_LIGHT:
        lights.append(EnergenieLight(2, config_entry.data.get(CONF_DEVICE_2_NAME), config_entry.entry_id))
    
    if config_entry.data.get("device_3_enabled", False) and config_entry.data.get(CONF_DEVICE_3_TYPE) == DEVICE_TYPE_LIGHT:
        lights.append(EnergenieLight(3, config_entry.data.get(CONF_DEVICE_3_NAME), config_entry.entry_id))
    
    if config_entry.data.get("device_4_enabled", False) and config_entry.data.get(CONF_DEVICE_4_TYPE) == DEVICE_TYPE_LIGHT:
        lights.append(EnergenieLight(4, config_entry.data.get(CONF_DEVICE_4_NAME), config_entry.entry_id))

    if lights:
        async_add_entities(lights, True)

class EnergenieLight(LightEntity):
    """Representation of an Energenie Light."""

    def __init__(self, device_num: int, name: str, entry_id: str) -> None:
        """Initialize the light."""
        self._device_num = device_num
        self._name = name
        self._entry_id = entry_id
        self._is_on = False
        self._attr_unique_id = f"{DOMAIN}_{entry_id}_light_{device_num}"

    @property
    def name(self) -> str:
        """Return the name of the light."""
        return self._name

    @property
    def is_on(self) -> bool:
        """Return true if light is on."""
        return self._is_on

    @property
    def device_info(self):
        """Return device information."""
        return {
            "identifiers": {(DOMAIN, self._entry_id)},
            "name": "Energenie ENER314-RT Controller",
            "manufacturer": "Energenie",
            "model": "ENER314-RT",
        }

    async def async_turn_on(self, **kwargs) -> None:
        """Turn the light on."""
        try:
            from gpiozero import Energenie
            device = Energenie(self._device_num)
            device.on()
            self._is_on = True
            self.async_write_ha_state()
            _LOGGER.info("Turned on %s (device %d)", self._name, self._device_num)
        except Exception as e:
            _LOGGER.error("Error turning on %s: %s", self._name, e)

    async def async_turn_off(self, **kwargs) -> None:
        """Turn the light off."""
        try:
            from gpiozero import Energenie
            device = Energenie(self._device_num)
            device.off()
            self._is_on = False
            self.async_write_ha_state()
            _LOGGER.info("Turned off %s (device %d)", self._name, self._device_num)
        except Exception as e:
            _LOGGER.error("Error turning off %s: %s", self._name, e)