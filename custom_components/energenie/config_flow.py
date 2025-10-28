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
            # Validate the input
            await self.async_set_unique_id("energenie_ener314rt")
            self._abort_if_unique_id_configured()
            
            return self.async_create_entry(
                title="Energenie ENER314-RT",
                data=user_input,
            )

        # Define the configuration schema
        data_schema = vol.Schema({
            vol.Required(CONF_DEVICE_1_NAME, default=DEFAULT_DEVICE_NAMES[1]): str,
            vol.Required(CONF_DEVICE_1_TYPE, default=DEVICE_TYPE_LIGHT): vol.In(DEVICE_TYPES),
            vol.Required(CONF_DEVICE_2_NAME, default=DEFAULT_DEVICE_NAMES[2]): str,
            vol.Required(CONF_DEVICE_2_TYPE, default=DEVICE_TYPE_LIGHT): vol.In(DEVICE_TYPES),
            vol.Required(CONF_DEVICE_3_NAME, default=DEFAULT_DEVICE_NAMES[3]): str,
            vol.Required(CONF_DEVICE_3_TYPE, default=DEVICE_TYPE_LIGHT): vol.In(DEVICE_TYPES),
            vol.Required(CONF_DEVICE_4_NAME, default=DEFAULT_DEVICE_NAMES[4]): str,
            vol.Required(CONF_DEVICE_4_TYPE, default=DEVICE_TYPE_LIGHT): vol.In(DEVICE_TYPES),
        })

        return self.async_show_form(
            step_id="user",
            data_schema=data_schema,
            errors=errors,
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