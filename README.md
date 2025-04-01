# ZenBot-Pi

[![PyPI version](https://badge.fury.io/py/zenbot-pi.svg)](https://badge.fury.io/py/zenbot-pi)
[![Python 3.10](https://img.shields.io/badge/python-3.10-blue.svg)](https://www.python.org/downloads/release/python-310/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A Python package for controlling Arduino-based motor robots over I2C communication from a Raspberry Pi or other Linux SBCs.

# Start Generation Here
[![Watch the video](https://img.youtube.com/vi/QkVqdz7QVy4/hqdefault.jpg)](https://www.youtube.com/watch?v=QkVqdz7QVy4)
# End Generation Here

## Features

- Simple control of DC motors connected to an Arduino
- I2C communication protocol for reliability
- Command-line interface for manual control
- Library for integration into your Python projects

## Installation

### From PyPI```bash
pip install zenbot-pi
```

### From Source

```bash
git clone https://github.com/yourusername/zenbot-pi.git
cd zenbot-pi
pip install -e .
```

## Hardware Setup

1. Connect your Raspberry Pi/Orange Pi to Arduino via I2C:
   - Pi SDA → Arduino A4 (SDA)
   - Pi SCL → Arduino A5 (SCL)
   - Pi GND → Arduino GND
# Start Generation Here
## Pinout Information

- **Motor Control Pins:**
  - `enA (Pin 6)`: Enables motor A.
  - `in1 (Pin 4)`: Controls the direction of motor A (input 1).
  - `in2 (Pin 5)`: Controls the direction of motor A (input 2).
  - `in3 (Pin 7)`: Controls the direction of motor B (input 1).
  - `in4 (Pin 8)`: Controls the direction of motor B (input 2).
  - `enB (Pin 9)`: Enables motor B.

- **Buzzer and Button Pins:**
  - `buzzer (Pin A0)`: Used to produce sound feedback.
  - `startButton (Pin 12)`: Button to stop the motors for safety.

- **I2C Communication:**
  - The Arduino uses the I2C address `0x08` for communication with the Raspberry Pi or other devices.
# End Generation Here

2. Make sure the Arduino is running the provided sketch (see `arduino_sketches` directory) with I2C slave address set to 0x08.

3. Enable I2C on your Raspberry Pi:
   ```bash
   sudo raspi-config
   ```
   Navigate to Interfacing Options → I2C → Enable

   For Orange Pi, use `sudo orangepi-config` or appropriate method.

## Using the CLI

The package provides a command-line interface:

```bash
# Run interactive control mode
zenbot-pi interactive

# Run test sequence
zenbot-pi test

# Send direct commands
zenbot-pi direct forward
zenbot-pi direct stop
zenbot-pi direct 5  # Set speed to 5

# Use different I2C bus or address
zenbot-pi --i2c-bus 1 --address 0x09 interactive
```

## Using the Library

Basic usage example:

```python
from zenbot import MotorController

# Create a controller, specifying I2C bus (default: 3) and address (default: 0x08)
controller = MotorController(i2c_bus=3, address=0x08)

# Test communication with Arduino
if controller.test_communication():
    # Set speed (0-9)
    controller.set_speed(5)
    
    # Move the robot
    controller.forward()
    
    # Wait a bit
    import time
    time.sleep(2)
    
    # Stop motors
    controller.stop()
    
    # Clean up when done
    controller.close()
```

## Available Commands

- `forward()` - Move robot forward
- `backward()` - Move robot backward
- `left()` - Turn robot left
- `right()` - Turn robot right
- `stop()` - Stop all motors
- `set_speed(level)` - Set speed level (0-9)
- `get_status()` - Get system status
- `send_command(cmd)` - Send a raw command character
- `close()` - Close I2C connection

## Arduino Setup

This library requires an Arduino running the provided sketch. The Arduino sketch:

1. Listens for commands on I2C bus (address 0x08 by default)
2. Controls motor driver shield/circuit based on received commands
3. Provides status feedback

## Troubleshooting

- Check I2C connection with `i2cdetect -y [bus_number]`
- Ensure Arduino has the correct I2C address (0x08 by default)
- Verify power supply is adequate for motors
- Check log file `zenbot.log` for debugging information

## License

MIT License - see LICENSE file for details

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request. 

