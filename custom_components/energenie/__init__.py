"""The Energenie ENER314-RT integration."""
import asyncio
import logging

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant, ServiceCall
from homeassistant.helpers import device_registry as dr
import voluptuous as vol

from .const import (
    DOMAIN,
    MANUFACTURER,
    MODEL,
    SERVICE_TURN_ON_ALL,
    SERVICE_TURN_OFF_ALL,
    DEVICE_TYPE_LIGHT,
    DEVICE_TYPE_SWITCH,
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

PLATFORMS = ["light", "switch"]

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up Energenie ENER314-RT from a config entry."""
    
    # Store configuration data
    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][entry.entry_id] = entry.data

    # Setup device registry
    device_registry = dr.async_get(hass)
    device_registry.async_get_or_create(
        config_entry_id=entry.entry_id,
        identifiers={(DOMAIN, entry.entry_id)},
        manufacturer=MANUFACTURER,
        model=MODEL,
        name="Energenie ENER314-RT Controller",
    )

    # Set up platforms
    for platform in PLATFORMS:
        hass.async_create_task(
            hass.config_entries.async_forward_entry_setup(entry, platform)
        )

    # Register services
    async def handle_turn_on_all(call: ServiceCall) -> None:
        """Handle turn on all devices service."""
        try:
            from gpiozero import Energenie
            for i in range(1, 5):
                device = Energenie(i)
                device.on()
                await asyncio.sleep(0.5)
            _LOGGER.info("All Energenie devices turned on")
        except Exception as e:
            _LOGGER.error("Error turning on all devices: %s", e)

    async def handle_turn_off_all(call: ServiceCall) -> None:
        """Handle turn off all devices service."""
        try:
            from gpiozero import Energenie
            for i in range(1, 5):
                device = Energenie(i)
                device.off()
                await asyncio.sleep(0.5)
            _LOGGER.info("All Energenie devices turned off")
        except Exception as e:
            _LOGGER.error("Error turning off all devices: %s", e)

    hass.services.async_register(
        DOMAIN, SERVICE_TURN_ON_ALL, handle_turn_on_all
    )
    hass.services.async_register(
        DOMAIN, SERVICE_TURN_OFF_ALL, handle_turn_off_all
    )

    return True

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    unload_ok = all(
        await asyncio.gather(
            *[
                hass.config_entries.async_forward_entry_unload(entry, platform)
                for platform in PLATFORMS
            ]
        )
    )

    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id)

    # Remove services
    hass.services.async_remove(DOMAIN, SERVICE_TURN_ON_ALL)
    hass.services.async_remove(DOMAIN, SERVICE_TURN_OFF_ALL)

    return unload_ok

async def async_reload_entry(hass: HomeAssistant, entry: ConfigEntry) -> None:
    """Reload config entry."""
    await async_unload_entry(hass, entry)
    await async_setup_entry(hass, entry)