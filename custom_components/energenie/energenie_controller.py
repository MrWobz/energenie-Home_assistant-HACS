#!/usr/bin/env python3
"""
Energenie Radio Control Device Controller using gpiozero
Supports both interactive menu and command line control
Controls radio switches, lights, sockets, and other Energenie devices

Designed for Raspberry Pi with Home Assistant integration
Compatible with shell_command and command_line platforms
"""

import argparse
import sys
import time
import json
import os
from gpiozero import Energenie

# Configuration file path
CONFIG_FILE = "energenie_config.json"

def load_config():
    """Load device configuration from JSON file"""
    default_config = {
        "devices": {
            "1": {"name": "Device 1", "type": "switch"},
            "2": {"name": "Device 2", "type": "switch"},
            "3": {"name": "Device 3", "type": "switch"},
            "4": {"name": "Device 4", "type": "switch"}
        }
    }
    
    try:
        if os.path.exists(CONFIG_FILE):
            with open(CONFIG_FILE, 'r') as f:
                return json.load(f)
        else:
            # Create default config file
            save_config(default_config)
            return default_config
    except Exception as e:
        print(f"Error loading config: {e}")
        return default_config

def save_config(config):
    """Save device configuration to JSON file"""
    try:
        with open(CONFIG_FILE, 'w') as f:
            json.dump(config, f, indent=2)
        return True
    except Exception as e:
        print(f"Error saving config: {e}")
        return False

def show_config_menu():
    """Display configuration menu"""
    config = load_config()
    print("\n" + "="*60)
    print("    Device Configuration")
    print("="*60)
    for device_id, device_info in config["devices"].items():
        print(f"{device_id}. {device_info['name']} ({device_info['type']})")
    print("\nConfiguration Options:")
    print("c1-c4: Configure device 1-4")
    print("s: Save current configuration")
    print("r: Reset to default configuration")
    print("b: Back to main menu")
    print("="*60)

def configure_device(device_num, config):
    """Configure a specific device"""
    device_id = str(device_num)
    current = config["devices"][device_id]
    
    print(f"\nCurrent configuration for Device {device_num}:")
    print(f"Name: {current['name']}")
    print(f"Type: {current['type']}")
    
    new_name = input(f"\nEnter new name for device {device_num} (or press Enter to keep '{current['name']}'): ").strip()
    if new_name:
        config["devices"][device_id]["name"] = new_name
    
    print("\nDevice types: switch, light, socket, fan, heater, other")
    new_type = input(f"Enter device type (or press Enter to keep '{current['type']}'): ").strip().lower()
    if new_type and new_type in ['switch', 'light', 'socket', 'fan', 'heater', 'other']:
        config["devices"][device_id]["type"] = new_type
    elif new_type and new_type not in ['switch', 'light', 'socket', 'fan', 'heater', 'other']:
        print("Invalid type! Keeping current type.")
    
    return config

def config_mode():
    """Run the configuration menu"""
    config = load_config()
    
    while True:
        show_config_menu()
        choice = input("\nEnter your choice: ").strip().lower()
        
        if choice == 'b':
            break
        elif choice == 's':
            if save_config(config):
                print("Configuration saved successfully!")
            else:
                print("Failed to save configuration!")
        elif choice == 'r':
            config = {
                "devices": {
                    "1": {"name": "Device 1", "type": "switch"},
                    "2": {"name": "Device 2", "type": "switch"},
                    "3": {"name": "Device 3", "type": "switch"},
                    "4": {"name": "Device 4", "type": "switch"}
                }
            }
            print("Configuration reset to defaults!")
        elif choice in ['c1', 'c2', 'c3', 'c4']:
            device_num = int(choice[1])
            config = configure_device(device_num, config)
        else:
            print("Invalid choice!")
        
        if choice != 'b':
            input("\nPress Enter to continue...")

def show_menu():
    """Display the interactive menu"""
    config = load_config()
    print("\n" + "="*60)
    print("    Energenie Radio Control Device Controller")
    print("="*60)
    
    for i in range(1, 5):
        device_info = config["devices"][str(i)]
        print(f"{i*2-1}. Turn ON {device_info['name']} ({device_info['type']})")
        print(f"{i*2}. Turn OFF {device_info['name']} ({device_info['type']})")
    
    print("9. Turn ON ALL devices")
    print("10. Turn OFF ALL devices")
    print("c. Configure devices")
    print("0. Exit")
    print("="*60)

def control_device(device_num, action, quiet=False):
    """Control a specific device"""
    config = load_config()
    
    try:
        if device_num == 0:  # All devices
            devices = [Energenie(1), Energenie(2), Energenie(3), Energenie(4)]
            for i, device in enumerate(devices, 1):
                device_info = config["devices"][str(i)]
                if action.lower() == 'on':
                    device.on()
                    if not quiet:
                        print(f"{device_info['name']} turned ON")
                else:
                    device.off()
                    if not quiet:
                        print(f"{device_info['name']} turned OFF")
                time.sleep(0.5)  # Small delay between commands
        else:
            device = Energenie(device_num)
            device_info = config["devices"][str(device_num)]
            if action.lower() == 'on':
                device.on()
                if not quiet:
                    print(f"{device_info['name']} turned ON")
            else:
                device.off()
                if not quiet:
                    print(f"{device_info['name']} turned OFF")
    
    except Exception as e:
        if not quiet:
            print(f"Error controlling {device_info.get('name', f'device {device_num}')}: {e}")
        return False
    
    return True

def interactive_mode():
    """Run the interactive menu"""
    while True:
        show_menu()
        try:
            choice = input("\nEnter your choice (0-10, c): ").strip().lower()
            
            if choice == '0':
                print("Goodbye!")
                break
            elif choice == 'c':
                config_mode()
            elif choice == '1':
                control_device(1, 'on')
            elif choice == '2':
                control_device(1, 'off')
            elif choice == '3':
                control_device(2, 'on')
            elif choice == '4':
                control_device(2, 'off')
            elif choice == '5':
                control_device(3, 'on')
            elif choice == '6':
                control_device(3, 'off')
            elif choice == '7':
                control_device(4, 'on')
            elif choice == '8':
                control_device(4, 'off')
            elif choice == '9':
                control_device(0, 'on')  # All devices
            elif choice == '10':
                control_device(0, 'off')  # All devices
            else:
                print("Invalid choice! Please enter a number between 0-10 or 'c' for configuration.")
            
            # Pause before showing menu again
            if choice != '0' and choice != 'c':
                input("\nPress Enter to continue...")
                
        except KeyboardInterrupt:
            print("\n\nExiting...")
            break
        except Exception as e:
            print(f"Error: {e}")

def main():
    """Main function"""
    parser = argparse.ArgumentParser(
        description="Control Energenie radio devices using gpiozero",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python energenie_controller.py --device 1 --action on
  python energenie_controller.py --device 2 --action off
  python energenie_controller.py --device all --action on
  python energenie_controller.py  (for interactive mode)
        """
    )
    
    parser.add_argument('--device', '-d', 
                       choices=['1', '2', '3', '4', 'all'],
                       help='Device number to control (1-4) or "all"')
    parser.add_argument('--action', '-a',
                       choices=['on', 'off'],
                       help='Action to perform (on/off)')
    parser.add_argument('--quiet', '-q',
                       action='store_true',
                       help='Suppress output (useful for Home Assistant)')
    parser.add_argument('--status', 
                       action='store_true',
                       help='Show device status and exit (for Home Assistant)')
    
    args = parser.parse_args()
    
    # Show status and exit (useful for Home Assistant sensors)
    if args.status:
        config = load_config()
        status_info = {
            "devices": {},
            "config_file": CONFIG_FILE,
            "config_exists": os.path.exists(CONFIG_FILE)
        }
        for device_id, device_info in config["devices"].items():
            status_info["devices"][device_id] = {
                "name": device_info["name"],
                "type": device_info["type"]
            }
        print(json.dumps(status_info, indent=2))
        sys.exit(0)
    
    # Check if running in command line mode
    if args.device and args.action:
        device_num = 0 if args.device == 'all' else int(args.device)
        success = control_device(device_num, args.action, args.quiet)
        sys.exit(0 if success else 1)
    
    # If no command line arguments or incomplete arguments, run interactive mode
    elif args.device or args.action:
        print("Error: Both --device and --action are required for command line mode")
        parser.print_help()
        sys.exit(1)
    else:
        print("Starting interactive mode...")
        interactive_mode()

if __name__ == "__main__":
    main()