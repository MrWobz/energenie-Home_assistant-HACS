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
    SERVICE_PAIR_DEVICE,
    SERVICE_LEARN_MODE,
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

PLATFORMS = ["light", "switch", "binary_sensor"]

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up Energenie ENER314-RT from a config entry."""
    
    _LOGGER.info("Starting Energenie integration setup...")
    _LOGGER.debug("Entry data: %s", entry.data)
    
    try:
        # Store configuration data
        hass.data.setdefault(DOMAIN, {})
        hass.data[DOMAIN][entry.entry_id] = entry.data
        _LOGGER.debug("Configuration data stored successfully")

        # Test pyenergenie availability and functionality
        _LOGGER.info("Testing pyenergenie availability...")
        try:
            import energenie
            # Test basic initialization
            energenie.init()
            _LOGGER.info("pyenergenie initialization successful")
            energenie.finished()
        except ImportError as e:
            _LOGGER.error("pyenergenie library not available: %s", e)
            raise Exception("pyenergenie library not available. Install with: pip install pyenergenie")
        except Exception as e:
            _LOGGER.warning("pyenergenie test failed (this may be normal if hardware not connected): %s", e)
            # Don't fail setup for hardware test failures - allow software testing

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
                import energenie
                energenie.init()
                
                # Get all configured devices from entry data
                config_data = hass.data[DOMAIN][entry.entry_id]
                num_devices = config_data.get("num_devices", 16)
                
                for i in range(1, num_devices + 1):
                    device_enabled_key = f"device_{i}_enabled"
                    if config_data.get(device_enabled_key, False):
                        energenie.switch_on(i)
                        await asyncio.sleep(0.5)
                        
                energenie.finished()
                _LOGGER.info("All enabled Energenie devices turned on")
            except Exception as e:
                _LOGGER.error("Error turning on all devices: %s", e)

        async def handle_pair_device(call: ServiceCall) -> None:
            """Handle device pairing service."""
            device_id = call.data.get("device_id", 1)
            duration = call.data.get("duration", 10)
            
            try:
                import energenie
                energenie.init()
                
                _LOGGER.info("Starting pairing mode for device %d for %d seconds", device_id, duration)
                _LOGGER.info("PUT YOUR ENERGENIE DEVICE INTO LEARN MODE NOW!")
                
                # Send repeated on/off signals to help device learn
                for i in range(duration):
                    energenie.switch_on(device_id)
                    await asyncio.sleep(0.5)
                    energenie.switch_off(device_id)
                    await asyncio.sleep(0.5)
                    _LOGGER.debug("Pairing signal %d/%d sent for device %d", i+1, duration, device_id)
                
                energenie.finished()
                _LOGGER.info("Pairing mode completed for device %d", device_id)
                
            except Exception as e:
                _LOGGER.error("Error during device pairing: %s", e)

        async def handle_learn_mode(call: ServiceCall) -> None:
            """Handle learn mode service - sends continuous signals."""
            device_id = call.data.get("device_id", 1)
            command = call.data.get("command", "on")  # "on" or "off"
            duration = call.data.get("duration", 20)
            
            try:
                import energenie
                energenie.init()
                
                _LOGGER.info("Starting learn mode: device %d, command %s, duration %d seconds", device_id, command, duration)
                _LOGGER.info("PUT YOUR ENERGENIE DEVICE INTO LEARN MODE NOW!")
                
                # Send repeated signals
                for i in range(duration * 2):  # Send every 0.5 seconds
                    if command == "on":
                        energenie.switch_on(device_id)
                    else:
                        energenie.switch_off(device_id)
                    await asyncio.sleep(0.5)
                    _LOGGER.debug("Learn signal %d sent for device %d (%s)", i+1, device_id, command)
                
                energenie.finished()
                _LOGGER.info("Learn mode completed for device %d", device_id)
                
            except Exception as e:
                _LOGGER.error("Error during learn mode: %s", e)

        async def handle_turn_off_all(call: ServiceCall) -> None:
            """Handle turn off all devices service."""
            try:
                import energenie
                energenie.init()
                
                # Get all configured devices from entry data
                config_data = hass.data[DOMAIN][entry.entry_id]
                num_devices = config_data.get("num_devices", 16)
                
                for i in range(1, num_devices + 1):
                    device_enabled_key = f"device_{i}_enabled"
                    if config_data.get(device_enabled_key, False):
                        energenie.switch_off(i)
                        await asyncio.sleep(0.5)
                        
                energenie.finished()
                _LOGGER.info("All enabled Energenie devices turned off")
            except Exception as e:
                _LOGGER.error("Error turning off all devices: %s", e)

        hass.services.async_register(
            DOMAIN, SERVICE_TURN_ON_ALL, handle_turn_on_all
        )
        hass.services.async_register(
            DOMAIN, SERVICE_TURN_OFF_ALL, handle_turn_off_all
        )
        hass.services.async_register(
            DOMAIN, SERVICE_PAIR_DEVICE, handle_pair_device
        )
        hass.services.async_register(
            DOMAIN, SERVICE_LEARN_MODE, handle_learn_mode
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
    hass.services.async_remove(DOMAIN, SERVICE_PAIR_DEVICE)
    hass.services.async_remove(DOMAIN, SERVICE_LEARN_MODE)

    return unload_ok

async def async_reload_entry(hass: HomeAssistant, entry: ConfigEntry) -> None:
    """Reload config entry."""
    await async_unload_entry(hass, entry)
    await async_setup_entry(hass, entry)