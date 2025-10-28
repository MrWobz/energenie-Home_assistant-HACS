# Device Compatibility Guide

## Compatible Energenie Devices

This integration supports multiple Energenie device models. Many devices with different model numbers are internally identical and work the same way.

### Smart Light Switches (Identical Functionality)
- **MIHO024** - Smart Light Switch (White)
- **MIHO026** - Smart Light Switch (Brushed Steel) 
- **MIHO025** - Smart Light Switch (Black Nickel)
- **MIHO008** - Smart Light Switch (Alternative model)

**Features:**
- Same internal circuitry and functionality
- Different physical styling/colors only
- Support up to 16 devices per ENER314-RT
- Can be configured as either Light or Switch entities
- Require learning/pairing with ENER314-RT transmitter

### Smart Plugs
- **MIHO002** - Smart Plug (Original)
- **MIHO005** - Smart Plug+ (with power monitoring)
- **MIHO006** - Smart Plug (Compact)

**Features:**
- Basic on/off control
- Support up to 4 devices per ENER314-RT
- Configure as Switch entities
- Require learning/pairing with ENER314-RT transmitter

### Motion Sensors
- **MIHO032** - Motion Sensor (PIR)
- **MIHO033** - Motion Sensor (Alternative model)

**Features:**
- Wireless motion detection
- Battery powered
- Send radio signals to ENER314-RT when motion detected
- Configure as Binary Sensor entities
- No pairing required (transmit-only devices)

### Door/Window Sensors
- **MIHO012** - Door/Window Sensor

**Features:**
- Open/close detection
- Battery powered
- Send radio signals when opened/closed
- Configure as Binary Sensor entities
- No pairing required (transmit-only devices)

## Device Configuration Tips

### For Smart Switches/Plugs (Receive-only devices):
1. **Put device in learning mode** (hold button until LED flashes)
2. **Use pairing service** in Home Assistant: `energenie.pair_device`
3. **Or use learn mode service** for specific commands: `energenie.learn_mode`
4. **Device LED should confirm** successful pairing

### For Sensors (Transmit-only devices):
1. **Enable motion sensor** in integration configuration
2. **Set correct sensor ID** (usually printed on device)
3. **Sensors automatically transmit** - no pairing needed
4. **Battery level affects** transmission range and reliability

### Entity Type Selection:
- **Light**: Shows with brightness icon, integrates with light controls
- **Switch**: Shows with power icon, integrates with switch controls  
- **Choice is cosmetic** - functionality is identical for smart switches

## Troubleshooting

### Device Not Responding:
1. Check device is in learning mode
2. Use longer pairing duration (20-30 seconds)
3. Ensure ENER314-RT is properly connected
4. Try different device slot numbers

### Motion Sensor Not Detected:
1. Verify sensor ID matches configuration
2. Check battery level in sensor
3. Ensure sensor is within range
4. Test sensor by triggering motion

### Multiple Identical Models:
- All MIHO024/026/025/008 devices work identically
- Use any available device slot (1-16)  
- Mix different model numbers freely
- Configuration is the same regardless of specific model