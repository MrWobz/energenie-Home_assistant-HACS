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
    
    _LOGGER.info("Starting Energenie integration setup...")
    _LOGGER.debug("Entry data: %s", entry.data)
    
    try:
        # Store configuration data
        hass.data.setdefault(DOMAIN, {})
        hass.data[DOMAIN][entry.entry_id] = entry.data
        _LOGGER.debug("Configuration data stored successfully")

        # Test GPIO availability and functionality
        _LOGGER.info("Testing GPIO availability...")
        try:
            from gpiozero import Device, LED
            # Test basic GPIO functionality with a safe pin
            test_led = LED(2)  # Use GPIO 2 for testing
            test_led.off()  # Ensure it's off
            _LOGGER.info("GPIO test successful - gpiozero library working")
        except ImportError as e:
            _LOGGER.error("gpiozero library not available: %s", e)
            raise Exception("GPIO library (gpiozero) not available. Ensure you're running on a Raspberry Pi with GPIO support.")
        except Exception as e:
            _LOGGER.warning("GPIO test failed (this may be normal if not on Raspberry Pi): %s", e)
            # Don't fail setup for GPIO test failures - allow software testing
            
        # Test Energenie module specifically
        _LOGGER.info("Testing Energenie module...")
        try:
            from gpiozero import Energenie
            # Don't actually create an Energenie device yet, just test import
            _LOGGER.info("Energenie module import successful")
        except ImportError as e:
            _LOGGER.error("Energenie module not available in gpiozero: %s", e)
            raise Exception("Energenie module not found in gpiozero library")
        except Exception as e:
            _LOGGER.warning("Energenie module test warning: %s", e)

        # Setup device registry
        device_registry = dr.async_get(hass)
        device_registry.async_get_or_create(
            config_entry_id=entry.entry_id,
            identifiers={(DOMAIN, entry.entry_id)},
            manufacturer=MANUFACTURER,
            model=MODEL,
            name="Energenie ENER314-RT Controller",
        )
        _LOGGER.debug("Device registry setup complete")

        # Set up platforms
        _LOGGER.info("Setting up platforms: %s", PLATFORMS)
        await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
        _LOGGER.debug("All platforms setup completed")

        # Register services
        _LOGGER.debug("Registering services")
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
        _LOGGER.debug("Services registered successfully")

        _LOGGER.info("Energenie integration setup completed successfully")
        return True
        
    except Exception as e:
        _LOGGER.exception("Failed to setup Energenie integration: %s", e)
        return False


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)

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