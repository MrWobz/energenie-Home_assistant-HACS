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
    CONF_MOTION_SENSOR_ENABLED,
    CONF_MOTION_SENSOR_NAME,
    CONF_MOTION_SENSOR_ID,
    DEVICE_TYPES,
    DEVICE_TYPE_LIGHT,
    DEVICE_TYPE_DESCRIPTIONS,
    COMPATIBLE_DEVICES,
    DEFAULT_DEVICE_NAMES,
    DEFAULT_MOTION_SENSOR_NAME,
    DEFAULT_MOTION_SENSOR_ID,
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
                
                # Test pyenergenie availability
                try:
                    _LOGGER.info("Testing pyenergenie library availability...")
                    import energenie
                    
                    # Test initialization
                    try:
                        energenie.init()
                        _LOGGER.info("pyenergenie initialization successful")
                        # Clean up
                        energenie.finished()
                    except Exception as init_error:
                        _LOGGER.warning("pyenergenie initialization test failed: %s", init_error)
                        # This might be normal if hardware isn't connected
                        
                    _LOGGER.info("pyenergenie tests completed successfully")
                    
                except ImportError as e:
                    _LOGGER.error("pyenergenie library not available: %s", e)
                    errors["base"] = "pyenergenie_not_available"
                except Exception as e:
                    _LOGGER.warning("pyenergenie test failed: %s", e)
                    errors["base"] = "pyenergenie_test_failed"
                
                if not errors:
                    return self.async_create_entry(
                        title="Energenie ENER314-RT",
                        data=user_input,
                    )
                    
            except Exception as e:
                _LOGGER.exception("Unexpected error during setup: %s", e)
                errors["base"] = "unknown"

        # Define the configuration schema - dynamic device configuration
        data_schema_fields = {}
        
        # Add option for number of devices to configure
        data_schema_fields[vol.Optional("num_devices", default=4)] = vol.In([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16])
        
        # Always show first 4 devices for compatibility
        for i in range(1, 5):
            data_schema_fields[vol.Optional(f"device_{i}_enabled", default=(i == 1))] = bool
            data_schema_fields[vol.Optional(f"device_{i}_name", default=DEFAULT_DEVICE_NAMES[i])] = str
            data_schema_fields[vol.Optional(f"device_{i}_type", default=DEVICE_TYPE_LIGHT)] = vol.In(DEVICE_TYPES)
        
        # Motion sensor configuration
        data_schema_fields[vol.Optional(CONF_MOTION_SENSOR_ENABLED, default=False)] = bool
        data_schema_fields[vol.Optional(CONF_MOTION_SENSOR_NAME, default=DEFAULT_MOTION_SENSOR_NAME)] = str
        data_schema_fields[vol.Optional(CONF_MOTION_SENSOR_ID, default=DEFAULT_MOTION_SENSOR_ID)] = str
        
        data_schema = vol.Schema(data_schema_fields)

        return self.async_show_form(
            step_id="user",
            data_schema=data_schema,
            errors=errors,
            description_placeholders={
                "pyenergenie_not_available": "pyenergenie library is not available. Install it with: pip install pyenergenie",
                "pyenergenie_test_failed": "pyenergenie library test failed. Check that your ENER314-RT board is properly connected and you have the correct permissions.",
                "unknown": "An unexpected error occurred during setup. Check the logs for more details.",
                "compatible_devices": self._get_compatible_devices_info()
            }
        )

    def _get_compatible_devices_info(self):
        """Generate device compatibility information for the UI."""
        info_lines = ["Compatible Energenie devices:"]
        
        for category, details in COMPATIBLE_DEVICES.items():
            models = ", ".join(details["models"])
            info_lines.append(f"• {details['description']}: {models}")
            if details["max_devices"] > 1:
                info_lines.append(f"  (Supports up to {details['max_devices']} devices)")
        
        info_lines.append("")
        info_lines.append("Device Types:")
        for dev_type, description in DEVICE_TYPE_DESCRIPTIONS.items():
            info_lines.append(f"• {description}")
            
        return "\n".join(info_lines)

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