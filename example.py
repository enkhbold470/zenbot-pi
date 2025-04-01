#!/usr/bin/env python3
"""
Example usage of the controlPI package for controlling an Arduino robot
"""
import time
from controlPI import MotorController

def simple_square_pattern():
    """Make the robot drive in a square pattern"""
    # Initialize the controller
    print("Initializing motor controller...")
    controller = MotorController(i2c_bus=3, address=0x08)
    
    try:
        # Start the system and set speed
        print("Starting robot...")
        controller.toggle_system()  # Turn on
        time.sleep(0.5)
        
        controller.set_speed(5)     # Medium speed
        time.sleep(0.5)
        
        # Execute a square pattern
        for i in range(4):
            print(f"Square side {i+1}/4...")
            
            # Move forward
            print("Moving forward")
            controller.forward()
            time.sleep(2)  # Drive for 2 seconds
            
            # Turn right 90 degrees
            print("Turning right")
            controller.right()
            time.sleep(1)  # Turn for 1 second
        
        # Stop and shutdown
        print("Square complete, stopping...")
        controller.stop()
        time.sleep(0.5)
        controller.toggle_system()  # Turn off
        
    except KeyboardInterrupt:
        print("\nProgram interrupted!")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        # Always ensure motors are stopped and connection closed
        print("Cleaning up...")
        controller.stop()
        controller.close()
        print("Done!")

if __name__ == "__main__":
    print("controlPI Example: Square Pattern")
    print("================================")
    
    # Run the demo
    simple_square_pattern() 