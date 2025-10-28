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
    
    # Get number of devices to check (default to 16 for full range)
    num_devices = config_entry.data.get("num_devices", 16)
    
    # Check all possible device slots up to the configured number
    for i in range(1, num_devices + 1):
        device_enabled_key = f"device_{i}_enabled"
        device_type_key = f"device_{i}_type" 
        device_name_key = f"device_{i}_name"
        
        # Only create lights for enabled devices of light type
        if config_entry.data.get(device_enabled_key, False) and config_entry.data.get(device_type_key) == DEVICE_TYPE_LIGHT:
            device_name = config_entry.data.get(device_name_key, f"Energenie Device {i}")
            lights.append(EnergenieLight(i, device_name, config_entry.entry_id))

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
            import energenie
            energenie.init()
            energenie.switch_on(self._device_num)
            energenie.finished()
            self._is_on = True
            self.async_write_ha_state()
            _LOGGER.info("Turned on %s (device %d)", self._name, self._device_num)
        except Exception as e:
            _LOGGER.error("Error turning on %s: %s", self._name, e)

    async def async_turn_off(self, **kwargs) -> None:
        """Turn the light off."""
        try:
            import energenie
            energenie.init()
            energenie.switch_off(self._device_num)
            energenie.finished()
            self._is_on = False
            self.async_write_ha_state()
            _LOGGER.info("Turned off %s (device %d)", self._name, self._device_num)
        except Exception as e:
            _LOGGER.error("Error turning off %s: %s", self._name, e)