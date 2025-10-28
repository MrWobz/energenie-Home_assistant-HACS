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
                
                # Process the setup data
                setup_data = {}
                
                # If user wants to set up first device
                if user_input.get("setup_device_now", True):
                    setup_data["device_1_enabled"] = True
                    setup_data[CONF_DEVICE_1_NAME] = user_input.get(CONF_DEVICE_1_NAME, DEFAULT_DEVICE_NAMES[1])
                    setup_data[CONF_DEVICE_1_TYPE] = user_input.get(CONF_DEVICE_1_TYPE, DEVICE_TYPE_LIGHT)
                
                # Motion sensor setup
                if user_input.get(CONF_MOTION_SENSOR_ENABLED, False):
                    setup_data[CONF_MOTION_SENSOR_ENABLED] = True
                    setup_data[CONF_MOTION_SENSOR_NAME] = user_input.get(CONF_MOTION_SENSOR_NAME, DEFAULT_MOTION_SENSOR_NAME)
                    setup_data[CONF_MOTION_SENSOR_ID] = user_input.get(CONF_MOTION_SENSOR_ID, DEFAULT_MOTION_SENSOR_ID)
                
                # Test required dependencies - but allow setup to continue
                dependencies_missing = []
                
                # Test RPi.GPIO (but don't fail setup)
                try:
                    import RPi.GPIO
                    _LOGGER.info("RPi.GPIO library found and imported successfully")
                except ImportError as e:
                    _LOGGER.warning("RPi.GPIO library not available: %s", e)
                    dependencies_missing.append("RPi.GPIO")
                
                # Test pyenergenie availability (but don't fail setup)
                try:
                    _LOGGER.info("Testing pyenergenie library availability...")
                    import energenie
                    _LOGGER.info("pyenergenie library found and imported successfully")
                    
                except ImportError as e:
                    _LOGGER.warning("pyenergenie library not available: %s", e)
                    dependencies_missing.append("pyenergenie")
                    
                except Exception as e:
                    _LOGGER.warning("pyenergenie library test warning: %s", e)
                
                # Log missing dependencies but allow setup to continue
                if dependencies_missing:
                    _LOGGER.info("Missing dependencies: %s - Home Assistant will attempt to install them automatically", dependencies_missing)
                    _LOGGER.info("If integration doesn't work after restart, check Home Assistant logs for installation errors")
                
                if not errors:
                    return self.async_create_entry(
                        title="Energenie ENER314-RT",
                        data=setup_data,
                    )
                    
            except Exception as e:
                _LOGGER.exception("Unexpected error during setup: %s", e)
                errors["base"] = "unknown"

        # Simplified initial configuration - just create the integration
        data_schema = vol.Schema({
            vol.Optional("setup_device_now", default=True): bool,
            vol.Optional(CONF_DEVICE_1_NAME, default=DEFAULT_DEVICE_NAMES[1]): str,
            vol.Optional(CONF_DEVICE_1_TYPE, default=DEVICE_TYPE_LIGHT): vol.In(DEVICE_TYPES),
            vol.Optional(CONF_MOTION_SENSOR_ENABLED, default=False): bool,
            vol.Optional(CONF_MOTION_SENSOR_NAME, default=DEFAULT_MOTION_SENSOR_NAME): str,
            vol.Optional(CONF_MOTION_SENSOR_ID, default=DEFAULT_MOTION_SENSOR_ID): str,
        })

        return self.async_show_form(
            step_id="user",
            data_schema=data_schema,
            errors=errors,
            description_placeholders={
                "setup_info": "The integration will be created now. Home Assistant will automatically install required dependencies (RPi.GPIO and pyenergenie) in the background.\n\nIf devices don't work after setup:\n1. Restart Home Assistant to complete dependency installation\n2. Check Settings → System → Logs for any installation errors\n3. The integration will show detailed error messages if dependencies are missing",
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
            # Merge new options with existing data
            new_data = {**self.config_entry.data}
            
            # Add new device if specified
            if user_input.get("add_device"):
                device_id = user_input.get("new_device_id", 2)
                device_name = user_input.get("new_device_name", f"Energenie Device {device_id}")
                device_type = user_input.get("new_device_type", DEVICE_TYPE_LIGHT)
                
                new_data[f"device_{device_id}_enabled"] = True
                new_data[f"device_{device_id}_name"] = device_name
                new_data[f"device_{device_id}_type"] = device_type
            
            # Update motion sensor if changed
            if "motion_sensor_enabled" in user_input:
                new_data[CONF_MOTION_SENSOR_ENABLED] = user_input["motion_sensor_enabled"]
                if user_input["motion_sensor_enabled"]:
                    new_data[CONF_MOTION_SENSOR_NAME] = user_input.get("motion_sensor_name", DEFAULT_MOTION_SENSOR_NAME)
                    new_data[CONF_MOTION_SENSOR_ID] = user_input.get("motion_sensor_id", DEFAULT_MOTION_SENSOR_ID)
            
            # Update the config entry
            self.hass.config_entries.async_update_entry(
                self.config_entry, data=new_data
            )
            
            return self.async_create_entry(title="", data={})

        # Get current configuration
        current_config = self.config_entry.data
        
        # Find next available device slot
        next_device_id = 2
        for i in range(2, 17):  # Check slots 2-16
            if not current_config.get(f"device_{i}_enabled", False):
                next_device_id = i
                break

        data_schema = vol.Schema({
            vol.Optional("add_device", default=False): bool,
            vol.Optional("new_device_id", default=next_device_id): vol.In(list(range(1, 17))),
            vol.Optional("new_device_name", default=f"Energenie Device {next_device_id}"): str,
            vol.Optional("new_device_type", default=DEVICE_TYPE_LIGHT): vol.In(DEVICE_TYPES),
            vol.Optional(
                "motion_sensor_enabled", 
                default=current_config.get(CONF_MOTION_SENSOR_ENABLED, False)
            ): bool,
            vol.Optional(
                "motion_sensor_name", 
                default=current_config.get(CONF_MOTION_SENSOR_NAME, DEFAULT_MOTION_SENSOR_NAME)
            ): str,
            vol.Optional(
                "motion_sensor_id", 
                default=current_config.get(CONF_MOTION_SENSOR_ID, DEFAULT_MOTION_SENSOR_ID)
            ): str,
        })

        return self.async_show_form(
            step_id="init",
            data_schema=data_schema,
            description_placeholders={
                "current_devices": self._get_current_devices_info()
            }
        )
    
    def _get_current_devices_info(self):
        """Get info about currently configured devices."""
        current_config = self.config_entry.data
        devices = []
        
        for i in range(1, 17):
            if current_config.get(f"device_{i}_enabled", False):
                name = current_config.get(f"device_{i}_name", f"Device {i}")
                device_type = current_config.get(f"device_{i}_type", "unknown")
                devices.append(f"Device {i}: {name} ({device_type})")
        
        if current_config.get(CONF_MOTION_SENSOR_ENABLED, False):
            sensor_name = current_config.get(CONF_MOTION_SENSOR_NAME, "Motion Sensor")
            devices.append(f"Motion Sensor: {sensor_name}")
        
        if not devices:
            return "No devices currently configured"
        
        return "Currently configured:\n" + "\n".join(devices)