# Energenie ENER314-RT Home Assistant Integration

A comprehensive Home Assistant custom integration for controlling Energenie devices using the ENER314-RT board.

## Features

- **Smart Switch/Light Control**: Control Energenie smart switches and plugs
- **Motion Detection**: Support for PIR motion sensors (MIHO032/MIHO033)
- **Device Pairing**: Built-in services for learning/pairing new devices
- **Flexible Configuration**: Support 1-16 devices per ENER314-RT board
- **Multiple Entity Types**: Configure devices as lights or switches
- **Comprehensive Logging**: Detailed setup and operation logging
- **HACS Compatible**: Easy installation and updates

## Supported Devices

### Smart Switches (Identical Functionality)
- **MIHO024** - Smart Light Switch (White)
- **MIHO026** - Smart Light Switch (Brushed Steel)
- **MIHO025** - Smart Light Switch (Black Nickel)  
- **MIHO008** - Smart Light Switch (Alternative model)

*Note: All these models are internally identical - only styling differs*

### Smart Plugs
- **MIHO002** - Smart Plug (Original)
- **MIHO005** - Smart Plug+ (with power monitoring)
- **MIHO006** - Smart Plug (Compact)

### Sensors
- **MIHO032** - Motion Sensor (PIR)
- **MIHO033** - Motion Sensor (Alternative model)
- **MIHO012** - Door/Window Sensor

## Requirements

- **Raspberry Pi** with GPIO access
- **ENER314-RT board** properly connected
- **Home Assistant** 2023.1.0 or later
- **HACS** (recommended) or manual installation

## Installation

### Via HACS (Recommended)

1. **Add Custom Repository**:
   - Open HACS → Integrations
   - Click three dots menu → Custom repositories
   - URL: `https://github.com/MrWobz/energenie-Home_assistant-HACS`
   - Category: Integration
   - Click ADD

2. **Install Integration**:
   - Search for "Energenie ENER314-RT" in HACS
   - Click Download
   - Restart Home Assistant

3. **Add Integration**:
   - Settings → Devices & Services → Add Integration
   - Search for "Energenie ENER314-RT"
   - Follow configuration wizard

### Manual Installation

1. **Copy Files**:
   ```bash
   # Copy the energenie folder to your custom_components directory
   cp -r custom_components/energenie /config/custom_components/
   ```

2. **Restart Home Assistant**

3. **Add Integration** via Settings → Devices & Services

## Configuration

### Initial Setup

1. **Enable Devices**: Choose which device slots to configure (1-16)
2. **Device Types**: Select Light or Switch for each device
3. **Custom Names**: Give devices meaningful names
4. **Motion Sensors**: Optionally enable and configure motion detection

### Device Pairing

Energenie switches/plugs are **receive-only** and must learn the ENER314-RT codes:

1. **Put device in learning mode** (hold button until LED flashes)
2. **Use pairing service**:
   ```yaml
   service: energenie.pair_device
   data:
     device_id: 1
     duration: 15
   ```
3. **Device LED confirms** successful pairing

### Motion Sensors

Motion sensors are **transmit-only** and require no pairing:

1. **Enable in configuration**
2. **Set sensor ID** (printed on device)
3. **Sensors automatically detected**

## Services

### Device Control
- `energenie.turn_on_all` - Turn on all configured devices
- `energenie.turn_off_all` - Turn off all configured devices

### Device Pairing
- `energenie.pair_device` - Pair new device (alternating on/off signals)
- `energenie.learn_mode` - Teach specific command (continuous signals)

### Service Examples

```yaml
# Pair a new device to slot 3
service: energenie.pair_device
data:
  device_id: 3
  duration: 20

# Teach "on" command to slot 1
service: energenie.learn_mode
data:
  device_id: 1
  command: "on"
  duration: 25

# Turn off all devices
service: energenie.turn_off_all
```

## Entity Types

### Light vs Switch

Both entity types control devices identically - choose based on UI preference:

- **Light Entities**: Show with brightness icon, integrate with light controls
- **Switch Entities**: Show with power icon, integrate with switch controls

### Motion Sensors

- **Binary Sensor**: Shows motion state (on/off)
- **Auto-clear**: Motion clears after 30 seconds
- **Attributes**: Shows sensor ID and last seen time

## Troubleshooting

### Device Not Responding
1. Check device is in learning mode
2. Increase pairing duration (20-30 seconds)
3. Verify ENER314-RT connection
4. Try different device slot

### Motion Sensor Issues
1. Verify sensor ID matches configuration
2. Check sensor battery level
3. Ensure sensor is within range
4. Test by triggering motion

### Library Issues
1. Check pyenergenie installation: `pip install git+https://github.com/whaleygeek/pyenergenie.git`
2. Verify GPIO permissions
3. Check ENER314-RT board connection
4. Review Home Assistant logs

## Hardware Setup

### ENER314-RT Connection
- Connect to Raspberry Pi GPIO pins as per Energenie documentation
- Ensure proper power supply
- Verify board LED indicators

### Device Limits
- **Smart Switches**: Up to 16 devices (MIHO024/026/025/008)
- **Smart Plugs**: Up to 4 devices (MIHO002/005/006)
- **Motion Sensors**: Multiple sensors supported

## Development

### Dependencies
- `pyenergenie` - Energenie control library
- Home Assistant 2023.1.0+

### Logging
Enable debug logging for troubleshooting:
```yaml
logger:
  logs:
    custom_components.energenie: debug
```

## Contributing

1. Fork the repository
2. Create feature branch
3. Test thoroughly
4. Submit pull request

## License

This project is licensed under the MIT License.

## Support

- **Issues**: [GitHub Issues](https://github.com/MrWobz/energenie-Home_assistant-HACS/issues)
- **Documentation**: [Device Compatibility Guide](DEVICE_COMPATIBILITY.md)
- **Home Assistant Community**: [Forum Discussion](https://community.home-assistant.io/)

## Changelog

### v1.0.3
- Added motion sensor support (MIHO032/MIHO033)
- Expanded device support (1-16 devices)
- Added device pairing services
- Migrated to pyenergenie library
- Added device compatibility mapping
- Improved error handling and logging

### v1.0.0
- Initial release
- Basic switch/light control
- HACS compatibility