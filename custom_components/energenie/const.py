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

# Device limits
MAX_DEVICES = 16  # Support up to 16 devices instead of just 4
MIN_DEVICE_ID = 1
CONF_DEVICE_2_ENABLED = "device_2_enabled"
CONF_DEVICE_3_ENABLED = "device_3_enabled"
CONF_DEVICE_4_ENABLED = "device_4_enabled"

# Device types
DEVICE_TYPE_LIGHT = "light"
DEVICE_TYPE_SWITCH = "switch"
DEVICE_TYPE_FAN = "fan"
DEVICE_TYPE_SOCKET = "socket"
DEVICE_TYPE_MOTION_SENSOR = "motion_sensor"

DEVICE_TYPES = [
    DEVICE_TYPE_LIGHT,
    DEVICE_TYPE_SWITCH,
    DEVICE_TYPE_FAN,
    DEVICE_TYPE_SOCKET,
    DEVICE_TYPE_MOTION_SENSOR,
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
SERVICE_PAIR_DEVICE = "pair_device"
SERVICE_LEARN_MODE = "learn_mode"
SERVICE_ADD_DEVICE = "add_device"

# Motion sensor configuration
CONF_MOTION_SENSOR_ENABLED = "motion_sensor_enabled"
CONF_MOTION_SENSOR_NAME = "motion_sensor_name"
CONF_MOTION_SENSOR_ID = "motion_sensor_id"

# Default motion sensor settings
DEFAULT_MOTION_SENSOR_NAME = "Energenie Motion Sensor"
DEFAULT_MOTION_SENSOR_ID = "MIHO032"

# Device compatibility mapping - devices that work the same way
COMPATIBLE_DEVICES = {
    "smart_plugs": {
        "models": ["MIHO002", "MIHO005", "MIHO006"],
        "description": "Smart Plugs - Basic on/off control",
        "max_devices": 4,
        "type": "switch"
    },
    "smart_switches": {
        "models": ["MIHO024", "MIHO026", "MIHO025", "MIHO008"],
        "description": "Smart Light Switches - Same internal design, different styles",
        "max_devices": 16,
        "type": "both"  # Can be used as switch or light
    },
    "motion_sensors": {
        "models": ["MIHO032", "MIHO033"],
        "description": "Motion Sensors - Wireless PIR detection",
        "max_devices": 1,
        "type": "binary_sensor"
    },
    "door_sensors": {
        "models": ["MIHO012"],
        "description": "Door/Window Sensors - Open/close detection", 
        "max_devices": 1,
        "type": "binary_sensor"
    }
}

# Device type descriptions for UI
DEVICE_TYPE_DESCRIPTIONS = {
    DEVICE_TYPE_LIGHT: "Light - Shows as light entity with brightness icon",
    DEVICE_TYPE_SWITCH: "Switch - Shows as switch entity with power icon",
    DEVICE_TYPE_MOTION_SENSOR: "Motion Sensor - Detects movement"
}