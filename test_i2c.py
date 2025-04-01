#!/usr/bin/env python3
import smbus2
import time
import sys

# Configuration
I2C_BUS = 3  # Change this based on your system (use i2cdetect to find)
ARDUINO_ADDRESS = 0x08  # The Arduino I2C address

# Test commands to send (in order)
COMMANDS = [
    ('?', 'Status request'),
    ('X', 'Toggle system ON'),
    ('5', 'Set speed to 5'),
    ('F', 'Move forward'),
    ('R', 'Turn right'),
    ('L', 'Turn left'),
    ('B', 'Move backward'),
    ('S', 'Stop motors'),
    ('X', 'Toggle system OFF')
]

def main():
    print("I2C Arduino Motor Controller Test")
    print("=================================")
    
    try:
        # Initialize I2C bus
        print(f"Opening I2C bus {I2C_BUS}...")
        bus = smbus2.SMBus(I2C_BUS)
        print("I2C bus opened successfully")
        
        # Test each command with delay
        for cmd, description in COMMANDS:
            try:
                print(f"\nSending: '{cmd}' - {description}")
                bus.write_byte(ARDUINO_ADDRESS, ord(cmd))
                time.sleep(1.5)  # Wait between commands
            except Exception as e:
                print(f"Error sending command: {e}")
        
        print("\nTest sequence completed")
        bus.close()
        
    except FileNotFoundError:
        print(f"ERROR: I2C Bus {I2C_BUS} not found.")
        print("Check if I2C is enabled in your system configuration.")
        sys.exit(1)
    except Exception as e:
        print(f"ERROR: {e}")
        sys.exit(1)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nTest interrupted.")
        sys.exit(0) 