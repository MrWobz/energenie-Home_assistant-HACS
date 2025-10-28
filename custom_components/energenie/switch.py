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
    config = hass.data[DOMAIN][config_entry.entry_id]
    
    switches = []
    
    # Create switch entities for devices configured as switches, fans, or sockets
    device_configs = [
        (1, config.get(CONF_DEVICE_1_NAME), config.get(CONF_DEVICE_1_TYPE)),
        (2, config.get(CONF_DEVICE_2_NAME), config.get(CONF_DEVICE_2_TYPE)),
        (3, config.get(CONF_DEVICE_3_NAME), config.get(CONF_DEVICE_3_TYPE)),
        (4, config.get(CONF_DEVICE_4_NAME), config.get(CONF_DEVICE_4_TYPE)),
    ]
    
    for device_num, device_name, device_type in device_configs:
        if device_type in [DEVICE_TYPE_SWITCH, DEVICE_TYPE_FAN, DEVICE_TYPE_SOCKET]:
            switches.append(EnergenieSwitch(device_num, device_name, device_type, config_entry.entry_id))
    
    async_add_entities(switches)

class EnergenieSwitch(SwitchEntity):
    """Representation of an Energenie Switch."""

    def __init__(self, device_num: int, name: str, device_type: str, entry_id: str) -> None:
        """Initialize the switch."""
        self._device_num = device_num
        self._name = name
        self._device_type = device_type
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
            from gpiozero import Energenie
            device = Energenie(self._device_num)
            device.on()
            self._is_on = True
            self.async_write_ha_state()
            _LOGGER.info("Turned on %s (device %d)", self._name, self._device_num)
        except Exception as e:
            _LOGGER.error("Error turning on %s: %s", self._name, e)

    async def async_turn_off(self, **kwargs) -> None:
        """Turn the switch off."""
        try:
            from gpiozero import Energenie
            device = Energenie(self._device_num)
            device.off()
            self._is_on = False
            self.async_write_ha_state()
            _LOGGER.info("Turned off %s (device %d)", self._name, self._device_num)
        except Exception as e:
            _LOGGER.error("Error turning off %s: %s", self._name, e)