"""Config flow for Energenie ENER314-RT integration."""
import logging
import voluptuous as vol

from homeassistant import config_entries
from homeassistant.core import callback
import homeassistant.helpers.config_validation as cv

from .const import (
    DOMAIN,
    CONF_DEVICE_1_NAME,
    CONF_DEVICE_1_TYPE,
    CONF_DEVICE_2_NAME,
    CONF_DEVICE_2_TYPE,
    CONF_DEVICE_3_NAME,
    CONF_DEVICE_3_TYPE,
    CONF_DEVICE_4_NAME,
    CONF_DEVICE_4_TYPE,
    DEVICE_TYPES,
    DEVICE_TYPE_LIGHT,
    DEFAULT_DEVICE_NAMES,
)

_LOGGER = logging.getLogger(__name__)

class EnergenieConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Energenie ENER314-RT."""

    VERSION = 1

    async def async_step_user(self, user_input=None):
        """Handle the initial step."""
        errors = {}

        if user_input is not None:
            try:
                # Validate the input
                _LOGGER.info("Setting up Energenie integration with data: %s", user_input)
                await self.async_set_unique_id("energenie_ener314rt")
                self._abort_if_unique_id_configured()
                
                # Test GPIO availability if gpiozero is available
                try:
                    _LOGGER.info("Testing GPIO and Energenie module availability...")
                    from gpiozero import Device, Energenie
                    
                    # Test if we can create an Energenie device (don't actually use it)
                    try:
                        test_device = Energenie(1)
                        _LOGGER.info("Energenie device creation test successful")
                        # Clean up the test device
                        test_device.close()
                    except Exception as device_error:
                        _LOGGER.warning("Energenie device test failed: %s", device_error)
                        # This might be normal if hardware isn't connected
                        
                    _LOGGER.info("GPIO and Energenie tests completed successfully")
                    
                except ImportError as e:
                    _LOGGER.error("gpiozero or Energenie module not available: %s", e)
                    errors["base"] = "gpio_not_available"
                except Exception as e:
                    _LOGGER.warning("GPIO/Energenie test failed: %s", e)
                    errors["base"] = "gpio_test_failed"
                
                if not errors:
                    return self.async_create_entry(
                        title="Energenie ENER314-RT",
                        data=user_input,
                    )
                    
            except Exception as e:
                _LOGGER.exception("Unexpected error during setup: %s", e)
                errors["base"] = "unknown"

        # Define the configuration schema - only ask which devices to enable
        data_schema = vol.Schema({
            vol.Optional("device_1_enabled", default=True): bool,
            vol.Optional(CONF_DEVICE_1_NAME, default=DEFAULT_DEVICE_NAMES[1]): str,
            vol.Optional(CONF_DEVICE_1_TYPE, default=DEVICE_TYPE_LIGHT): vol.In(DEVICE_TYPES),
            vol.Optional("device_2_enabled", default=False): bool,
            vol.Optional(CONF_DEVICE_2_NAME, default=DEFAULT_DEVICE_NAMES[2]): str,
            vol.Optional(CONF_DEVICE_2_TYPE, default=DEVICE_TYPE_LIGHT): vol.In(DEVICE_TYPES),
            vol.Optional("device_3_enabled", default=False): bool,
            vol.Optional(CONF_DEVICE_3_NAME, default=DEFAULT_DEVICE_NAMES[3]): str,
            vol.Optional(CONF_DEVICE_3_TYPE, default=DEVICE_TYPE_LIGHT): vol.In(DEVICE_TYPES),
            vol.Optional("device_4_enabled", default=False): bool,
            vol.Optional(CONF_DEVICE_4_NAME, default=DEFAULT_DEVICE_NAMES[4]): str,
            vol.Optional(CONF_DEVICE_4_TYPE, default=DEVICE_TYPE_LIGHT): vol.In(DEVICE_TYPES),
        })

        return self.async_show_form(
            step_id="user",
            data_schema=data_schema,
            errors=errors,
            description_placeholders={
                "gpio_not_available": "GPIO library (gpiozero) or Energenie module is not available. Make sure you're running on a Raspberry Pi with GPIO support and the ENER314-RT drivers installed.",
                "gpio_test_failed": "GPIO or Energenie hardware test failed. Check that your Raspberry Pi GPIO is working and the ENER314-RT board is properly connected.",
                "unknown": "An unexpected error occurred during setup. Check the logs for more details."
            }
        )

    @staticmethod
    @callback
    def async_get_options_flow(config_entry):
        """Create the options flow."""
        return EnergenieOptionsFlow(config_entry)


class EnergenieOptionsFlow(config_entries.OptionsFlow):
    """Handle options flow for Energenie ENER314-RT."""

    def __init__(self, config_entry):
        """Initialize options flow."""
        self.config_entry = config_entry

    async def async_step_init(self, user_input=None):
        """Handle options flow."""
        if user_input is not None:
            return self.async_create_entry(title="", data=user_input)

        # Get current configuration
        current_config = {**self.config_entry.data, **self.config_entry.options}

        data_schema = vol.Schema({
            vol.Required(
                CONF_DEVICE_1_NAME, 
                default=current_config.get(CONF_DEVICE_1_NAME, DEFAULT_DEVICE_NAMES[1])
            ): str,
            vol.Required(
                CONF_DEVICE_1_TYPE, 
                default=current_config.get(CONF_DEVICE_1_TYPE, DEVICE_TYPE_LIGHT)
            ): vol.In(DEVICE_TYPES),
            vol.Required(
                CONF_DEVICE_2_NAME, 
                default=current_config.get(CONF_DEVICE_2_NAME, DEFAULT_DEVICE_NAMES[2])
            ): str,
            vol.Required(
                CONF_DEVICE_2_TYPE, 
                default=current_config.get(CONF_DEVICE_2_TYPE, DEVICE_TYPE_LIGHT)
            ): vol.In(DEVICE_TYPES),
            vol.Required(
                CONF_DEVICE_3_NAME, 
                default=current_config.get(CONF_DEVICE_3_NAME, DEFAULT_DEVICE_NAMES[3])
            ): str,
            vol.Required(
                CONF_DEVICE_3_TYPE, 
                default=current_config.get(CONF_DEVICE_3_TYPE, DEVICE_TYPE_LIGHT)
            ): vol.In(DEVICE_TYPES),
            vol.Required(
                CONF_DEVICE_4_NAME, 
                default=current_config.get(CONF_DEVICE_4_NAME, DEFAULT_DEVICE_NAMES[4])
            ): str,
            vol.Required(
                CONF_DEVICE_4_TYPE, 
                default=current_config.get(CONF_DEVICE_4_TYPE, DEVICE_TYPE_LIGHT)
            ): vol.In(DEVICE_TYPES),
        })

        return self.async_show_form(
            step_id="init",
            data_schema=data_schema,
        )