# Energenie ENER314-RT Home Assistant Integration

A Home Assistant custom integration for controlling Energenie ENER314-RT radio controlled devices (lights, switches, sockets, fans) via GPIO on Raspberry Pi.

## Features

- 🎛️ **UI Configuration** - Configure all devices through Home Assistant's web interface
- 🔄 **Auto-Discovery** - Devices automatically appear as lights or switches based on configuration
- ⚙️ **Reconfigurable** - Change device names and types anytime through integration options
- 🛠️ **Built-in Services** - Turn all devices on/off with single service calls
- 📱 **Full HA Integration** - Works with automations, scenes, voice assistants, and mobile app

## Requirements

- Raspberry Pi with Home Assistant
- Energenie ENER314-RT board
- Python `gpiozero` library (automatically installed)

## Installation

### Via HACS (Recommended)

1. Open HACS in Home Assistant
2. Go to "Integrations"
3. Click the three dots menu → "Custom repositories"
4. Add this repository URL: `https://github.com/MrWobz/energenie-Home_assistant-HACS`
5. Select category "Integration"
6. Click "Add"
7. Find "Energenie ENER314-RT" in HACS and install
8. Restart Home Assistant

### Manual Installation

1. Download the `custom_components/energenie` folder from this repository
2. Copy it to your Home Assistant `config/custom_components/` directory
3. Restart Home Assistant

## Setup

1. Go to **Configuration** → **Integrations**
2. Click **"+ Add Integration"**
3. Search for **"Energenie ENER314-RT"**
4. Configure your 4 devices:
   - Set device names (e.g., "Living Room Light", "Kitchen Switch")
   - Choose device types (light, switch, fan, socket)
5. Click **"Submit"**

## Usage

### Devices
- **Lights**: Configured devices appear as light entities
- **Switches/Sockets/Fans**: Configured devices appear as switch entities with appropriate icons

### Services
- `energenie.turn_on_all` - Turn on all 4 devices
- `energenie.turn_off_all` - Turn off all 4 devices

### Automation Example
```yaml
automation:
  - alias: "Turn on lights at sunset"
    trigger:
      platform: sun
      event: sunset
    action:
      service: energenie.turn_on_all
```

### Voice Control
Works automatically with Alexa and Google Assistant once configured.

## Device Configuration

You can reconfigure device names and types anytime:

1. Go to **Configuration** → **Integrations**
2. Find **"Energenie ENER314-RT"**
3. Click **"Configure"**
4. Update names and types as needed

## Supported Device Types

- **Light** - Appears as light entity with on/off control
- **Switch** - Appears as switch entity 
- **Fan** - Appears as switch entity with fan icon
- **Socket** - Appears as switch entity with socket icon

## Troubleshooting

### GPIO Permissions
If you get permission errors, ensure Home Assistant can access GPIO:
```bash
sudo usermod -a -G gpio homeassistant
```

### gpiozero Installation
The integration automatically requires gpiozero, but if needed manually:
```bash
pip3 install gpiozero
```

## Development

This integration follows Home Assistant's development guidelines and includes:
- Config flow for UI setup
- Options flow for reconfiguration  
- Proper device registry integration
- Service definitions
- Platform separation (lights vs switches)

## License

MIT License - see LICENSE file for details.

## Contributing

Pull requests welcome! Please ensure code follows Home Assistant standards.