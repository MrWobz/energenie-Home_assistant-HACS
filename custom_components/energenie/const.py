"""Constants for the Energenie ENER314-RT integration."""

DOMAIN = "energenie"
MANUFACTURER = "Energenie"
MODEL = "ENER314-RT"

# Configuration keys
CONF_DEVICE_1_NAME = "device_1_name"
CONF_DEVICE_1_TYPE = "device_1_type"
CONF_DEVICE_2_NAME = "device_2_name"
CONF_DEVICE_2_TYPE = "device_2_type"
CONF_DEVICE_3_NAME = "device_3_name"
CONF_DEVICE_3_TYPE = "device_3_type"
CONF_DEVICE_4_NAME = "device_4_name"
CONF_DEVICE_4_TYPE = "device_4_type"

# Device types
DEVICE_TYPE_LIGHT = "light"
DEVICE_TYPE_SWITCH = "switch"
DEVICE_TYPE_FAN = "fan"
DEVICE_TYPE_SOCKET = "socket"

DEVICE_TYPES = [
    DEVICE_TYPE_LIGHT,
    DEVICE_TYPE_SWITCH,
    DEVICE_TYPE_FAN,
    DEVICE_TYPE_SOCKET,
]

# Default device names
DEFAULT_DEVICE_NAMES = {
    1: "Energenie Device 1",
    2: "Energenie Device 2", 
    3: "Energenie Device 3",
    4: "Energenie Device 4",
}

# Services
SERVICE_TURN_ON_ALL = "turn_on_all"
SERVICE_TURN_OFF_ALL = "turn_off_all"