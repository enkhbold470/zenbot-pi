#!/usr/bin/env python3
"""
Simple example demonstrating how to use the zenbot-pi package.
"""
import time
import logging
from zenbot import MotorController

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s'
)

def drive_square_pattern():
    """Drive in a square pattern."""
    print("ZenBot-Pi Example: Drive in a Square Pattern")
    print("===========================================")
    
    # Initialize the controller with your I2C bus and Arduino address
    # For Orange Pi, I2C bus is often 3, for Raspberry Pi it's often 1
    controller = MotorController(i2c_bus=3, address=0x08)
    
    try:
        # Test communication with the Arduino
        if not controller.test_communication():
            print("Failed to communicate with Arduino. Check connections and address.")
            return
        
        # Set motor speed (0-9)
        controller.set_speed(6)
        print("Speed set to 6")
        time.sleep(1)
        
        # Drive in a square pattern (4 sides)
        for side in range(4):
            print(f"\nDriving side {side+1} of the square")
            
            # Move forward for 2 seconds
            print("Moving forward...")
            controller.forward()
            time.sleep(2)
            
            # Turn right for 1 second
            print("Turning right...")
            controller.right()
            time.sleep(1)
        
        # Stop motors when done
        print("\nSquare pattern complete!")
        controller.stop()
        
    except KeyboardInterrupt:
        print("\nProgram interrupted!")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        # Always ensure motors are stopped and connection is closed
        controller.stop()
        controller.close()

if __name__ == "__main__":
    drive_square_pattern() 