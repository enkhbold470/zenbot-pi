#!/usr/bin/env python3
import time
import logging
import sys
from motor_controller import MotorController

def run_test_sequence():
    """Run a basic test sequence"""
    logger = logging.getLogger("MotorController")
    logger.info("===== Starting Motor Controller Test =====")
   
    # Create controller - modify I2C bus as needed for your setup
    controller = MotorController(i2c_bus=3, address=0x08)
   
    try:
        # Test communication
        if not controller.test_communication():
            logger.error("Failed to communicate with Arduino")
            return
           
        print("\nSystem is always active in this version.")
        print("Beginning motor test sequence...\n")
       
        # Test movement
        logger.info("Testing movement commands")
       
        controller.set_speed(5)  # Set medium speed
        time.sleep(0.5)
        print("Speed set to 5 (medium)")
       
        print("Moving forward for 1 second...")
        controller.forward()
        time.sleep(1)
       
        print("Turning right for 1 second...")
        controller.right()
        time.sleep(1)
       
        print("Moving backward for 1 second...")
        controller.backward()
        time.sleep(1)
       
        print("Turning left for 1 second...")
        controller.left()
        time.sleep(1)
       
        print("Stopping motors...")
        controller.stop()
        time.sleep(0.5)
       
        print("\nTest sequence complete!")
       
    except Exception as e:
        logger.error(f"Error during testing: {str(e)}")
    finally:
        # Stop motors and close connection
        controller.stop()
        controller.close()
        logger.info("===== Test Complete =====")

def interactive_mode():
    """Start an interactive control mode"""
    logger = logging.getLogger("MotorController")
    logger.info("===== Starting Interactive Control Mode =====")
   
    # Create controller - modify I2C bus as needed for your setup
    controller = MotorController(i2c_bus=3, address=0x08)
   
    # Test communication
    if not controller.test_communication():
        logger.error("Failed to communicate with Arduino")
        return
   
    print("\n🤖 Interactive Control Mode 🤖")
    print("-----------------------------")
    print("System is always active in this version!")
    print("Commands:")
    print("  F - Move Forward")
    print("  B - Move Backward")
    print("  L - Turn Left")
    print("  R - Turn Right")
    print("  S - Stop")
    print("  0-9 - Set Speed")
    print("  ? - Get Status")
    print("  Q - Quit")
    print("")
   
    try:
        while True:
            cmd = input("Enter command: ").strip().upper()
           
            if cmd == 'Q':
                break
            
            elif cmd == '?':
                print("Status: ACTIVE")
                controller.send_command(cmd)
                
            elif cmd in ['F', 'B', 'L', 'R', 'S'] or cmd.isdigit():
                response = controller.send_command(cmd)
                print(f"Response: {response}")
                
            else:
                print("Invalid command")
               
    except KeyboardInterrupt:
        print("\nExiting...")
    finally:
        # Stop motors and close connection
        controller.stop()
        controller.close()
        logger.info("===== Interactive Mode Ended =====")

if __name__ == "__main__":
    # Configure logging
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s [%(levelname)s] %(message)s',
        handlers=[
            logging.FileHandler("motor_controller.log"),
            logging.StreamHandler(sys.stdout)
        ]
    )
    
    print("\nArduino Motor Controller")
    print("1. Run test sequence")
    print("2. Start interactive mode")
    choice = input("Select an option (1/2): ").strip()
   
    if choice == '1':
        run_test_sequence()
    elif choice == '2':
        interactive_mode()
    else:
        print("Invalid choice")
