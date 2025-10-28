"""Energenie ENER314-RT Switch platform."""
import asyncio
import logging

from homeassistant.components.switch import SwitchEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import (
    DOMAIN,
    DEVICE_TYPE_SWITCH,
    DEVICE_TYPE_FAN,
    DEVICE_TYPE_SOCKET,
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
    """Set up Energenie switches from a config entry."""
    switches = []
    
    # Get number of devices to check (default to 16 for full range)
    num_devices = config_entry.data.get("num_devices", 16)
    
    # Check all possible device slots up to the configured number
    for i in range(1, num_devices + 1):
        device_enabled_key = f"device_{i}_enabled"
        device_type_key = f"device_{i}_type" 
        device_name_key = f"device_{i}_name"
        
        # Only create switches for enabled devices of switch type
        if config_entry.data.get(device_enabled_key, False) and config_entry.data.get(device_type_key) == DEVICE_TYPE_SWITCH:
            device_name = config_entry.data.get(device_name_key, f"Energenie Device {i}")
            switches.append(EnergenieSwitch(i, device_name, config_entry.entry_id))

    if switches:
        async_add_entities(switches, True)

class EnergenieSwitch(SwitchEntity):
    """Representation of an Energenie Switch."""

    def __init__(self, device_num: int, name: str, entry_id: str) -> None:
        """Initialize the switch."""
        self._device_num = device_num
        self._name = name
        self._entry_id = entry_id
        self._is_on = False
        self._attr_unique_id = f"{DOMAIN}_{entry_id}_switch_{device_num}"

    @property
    def name(self) -> str:
        """Return the name of the switch."""
        return self._name

    @property
    def is_on(self) -> bool:
        """Return true if switch is on."""
        return self._is_on

    @property
    def icon(self) -> str:
        """Return the icon for the switch."""
        if self._device_type == DEVICE_TYPE_FAN:
            return "mdi:fan"
        elif self._device_type == DEVICE_TYPE_SOCKET:
            return "mdi:power-socket-uk"
        else:
            return "mdi:toggle-switch"

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
        """Turn the switch on."""
        try:
            import energenie
        except ImportError as e:
            _LOGGER.error("pyenergenie library not available: %s", e)
            _LOGGER.error("Cannot control device - pyenergenie library is required")
            return
            
        try:
            energenie.init()
            energenie.switch_on(self._device_num)
            energenie.finished()
            self._is_on = True
            self.async_write_ha_state()
            _LOGGER.info("Turned on %s (device %d)", self._name, self._device_num)
        except Exception as e:
            _LOGGER.error("Error turning on %s: %s", self._name, e)

    async def async_turn_off(self, **kwargs) -> None:
        """Turn the switch off."""
        try:
            import energenie
        except ImportError as e:
            _LOGGER.error("pyenergenie library not available: %s", e)
            _LOGGER.error("Cannot control device - pyenergenie library is required")
            return
            
        try:
            energenie.init()
            energenie.switch_off(self._device_num)
            energenie.finished()
            self._is_on = False
            self.async_write_ha_state()
            _LOGGER.info("Turned off %s (device %d)", self._name, self._device_num)
        except Exception as e:
            _LOGGER.error("Error turning off %s: %s", self._name, e)