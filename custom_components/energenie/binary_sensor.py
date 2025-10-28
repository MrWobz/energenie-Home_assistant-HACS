"""Binary sensor platform for Energenie ENER314-RT integration."""
import logging
import asyncio
from datetime import timedelta

from homeassistant.components.binary_sensor import BinarySensorEntity, BinarySensorDeviceClass
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.event import async_track_time_interval
from homeassistant.util import dt as dt_util

from .const import (
    DOMAIN,
    MANUFACTURER,
    MODEL,
    CONF_MOTION_SENSOR_ENABLED,
    CONF_MOTION_SENSOR_NAME,
    CONF_MOTION_SENSOR_ID,
    DEFAULT_MOTION_SENSOR_NAME,
    DEFAULT_MOTION_SENSOR_ID,
)

_LOGGER = logging.getLogger(__name__)

SCAN_INTERVAL = timedelta(seconds=5)  # Check for messages every 5 seconds

async def async_setup_entry(hass, config_entry, async_add_entities):
    """Set up Energenie motion sensors from a config entry."""
    sensors = []
    
    # Only create motion sensor if enabled
    if config_entry.data.get(CONF_MOTION_SENSOR_ENABLED, False):
        sensor_name = config_entry.data.get(CONF_MOTION_SENSOR_NAME, DEFAULT_MOTION_SENSOR_NAME)
        sensor_id = config_entry.data.get(CONF_MOTION_SENSOR_ID, DEFAULT_MOTION_SENSOR_ID)
        sensors.append(EnergenieMotionSensor(sensor_name, sensor_id, config_entry.entry_id))

    if sensors:
        async_add_entities(sensors, True)


class EnergenieMotionSensor(BinarySensorEntity):
    """Representation of an Energenie motion sensor."""

    def __init__(self, name, sensor_id, config_entry_id):
        """Initialize the motion sensor."""
        self._name = name
        self._sensor_id = sensor_id
        self._config_entry_id = config_entry_id
        self._is_on = False
        self._last_seen = None
        self._unique_id = f"energenie_motion_{sensor_id}"
        self._listening = False
        self._unsub_timer = None

    @property
    def name(self):
        """Return the name of the sensor."""
        return self._name

    @property
    def unique_id(self):
        """Return a unique ID."""
        return self._unique_id

    @property
    def is_on(self):
        """Return true if motion is detected."""
        return self._is_on

    @property
    def device_class(self):
        """Return the device class."""
        return BinarySensorDeviceClass.MOTION

    @property
    def device_info(self):
        """Return device information."""
        return {
            "identifiers": {(DOMAIN, self._config_entry_id)},
            "name": "Energenie ENER314-RT Controller",
            "manufacturer": MANUFACTURER,
            "model": MODEL,
        }

    @property
    def extra_state_attributes(self):
        """Return additional state attributes."""
        return {
            "sensor_id": self._sensor_id,
            "last_seen": self._last_seen,
        }

    async def async_added_to_hass(self):
        """Start listening for motion sensor messages when added to hass."""
        await super().async_added_to_hass()
        await self._start_listening()

    async def async_will_remove_from_hass(self):
        """Stop listening when removed."""
        await self._stop_listening()

    async def _start_listening(self):
        """Start listening for motion sensor messages."""
        if self._listening:
            return
            
        _LOGGER.info("Starting motion sensor listener for %s", self._sensor_id)
        self._listening = True
        
        # Set up periodic checking for messages
        self._unsub_timer = async_track_time_interval(
            self.hass, self._check_for_messages, SCAN_INTERVAL
        )

    async def _stop_listening(self):
        """Stop listening for motion sensor messages."""
        if not self._listening:
            return
            
        _LOGGER.info("Stopping motion sensor listener for %s", self._sensor_id)
        self._listening = False
        
        if self._unsub_timer:
            self._unsub_timer()
            self._unsub_timer = None

    @callback
    async def _check_for_messages(self, now=None):
        """Check for incoming motion sensor messages."""
        try:
            import energenie
            
            # Initialize energenie for receiving
            energenie.init()
            
            # Check for any incoming messages
            msg = energenie.receive()
            if msg:
                # Check if this message is from our motion sensor
                if hasattr(msg, 'sensor_id') and str(msg.sensor_id) == str(self._sensor_id):
                    await self._handle_motion_message(msg)
                elif hasattr(msg, 'device_id') and str(msg.device_id) == str(self._sensor_id):
                    await self._handle_motion_message(msg)
                    
            energenie.finished()
            
        except Exception as e:
            _LOGGER.error("Error checking for motion sensor messages: %s", e)

    async def _handle_motion_message(self, msg):
        """Handle a motion sensor message."""
        try:
            _LOGGER.debug("Received motion sensor message: %s", msg)
            
            # Update last seen time
            self._last_seen = dt_util.utcnow().isoformat()
            
            # Check if this is a motion detection message
            motion_detected = False
            
            if hasattr(msg, 'motion') and msg.motion:
                motion_detected = True
            elif hasattr(msg, 'switch') and msg.switch:
                motion_detected = True
            elif hasattr(msg, 'state') and msg.state:
                motion_detected = True
                
            # Update state if changed
            if motion_detected != self._is_on:
                self._is_on = motion_detected
                self.async_write_ha_state()
                _LOGGER.info("Motion sensor %s: %s", self._sensor_id, "detected" if motion_detected else "cleared")
                
            # Auto-clear motion after 30 seconds if no new messages
            if motion_detected:
                self.hass.loop.call_later(30, self._auto_clear_motion)
                
        except Exception as e:
            _LOGGER.error("Error handling motion sensor message: %s", e)

    @callback
    def _auto_clear_motion(self):
        """Automatically clear motion detection after timeout."""
        if self._is_on:
            self._is_on = False
            self.async_write_ha_state()
            _LOGGER.debug("Auto-cleared motion for sensor %s", self._sensor_id)