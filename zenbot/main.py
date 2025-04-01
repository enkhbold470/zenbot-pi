#!/usr/bin/env python3
"""
ZenBot-Pi - I2C Motor Controller CLI Tool
"""
import time
import logging
import sys
import argparse
from .motor_controller import MotorController

def run_test_sequence(i2c_bus=3, address=0x08):
    """Run a basic test sequence"""
    logger = logging.getLogger(__name__)
    logger.info("===== Starting Motor Controller Test =====")
   
    # Create controller with the specified I2C bus and address
    controller = MotorController(i2c_bus=i2c_bus, address=address)
   
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

def interactive_mode(i2c_bus=3, address=0x08):
    """Start an interactive control mode"""
    logger = logging.getLogger(__name__)
    logger.info("===== Starting Interactive Control Mode =====")
   
    # Create controller with the specified I2C bus and address
    controller = MotorController(i2c_bus=i2c_bus, address=address)
   
    # Test communication
    if not controller.test_communication():
        logger.error("Failed to communicate with Arduino")
        return
   
    print("\n🤖 ZenBot-Pi Interactive Control Mode 🤖")
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

def direct_command(command, i2c_bus=3, address=0x08):
    """Send a direct command to the motor controller"""
    logger = logging.getLogger(__name__)
    logger.info(f"Sending direct command: {command}")
    
    controller = MotorController(i2c_bus=i2c_bus, address=address)
    
    try:
        # Test communication
        if not controller.test_communication():
            logger.error("Failed to communicate with Arduino")
            return
            
        # Send the command
        if command == "forward":
            response = controller.forward()
        elif command == "backward":
            response = controller.backward()
        elif command == "left":
            response = controller.left()
        elif command == "right":
            response = controller.right()
        elif command == "stop":
            response = controller.stop()
        elif command.isdigit() and 0 <= int(command) <= 9:
            response = controller.set_speed(int(command))
        elif command == "status":
            response = controller.get_status()
        else:
            print(f"Unknown command: {command}")
            return
            
        print(f"Response: {response}")
        
    except Exception as e:
        logger.error(f"Error: {str(e)}")
    finally:
        # Close connection
        controller.close()

def setup_logging(level=logging.INFO):
    """Set up logging configuration"""
    logging.basicConfig(
        level=level,
        format='%(asctime)s [%(levelname)s] %(message)s',
        handlers=[
            logging.FileHandler("zenbot-pi.log"),
            logging.StreamHandler(sys.stdout)
        ]
    )

def main():
    """Main CLI entry point"""
    parser = argparse.ArgumentParser(
        description="ZenBot-Pi - I2C Motor Controller for Raspberry Pi/Arduino robots"
    )
    
    # Add arguments
    parser.add_argument(
        "--i2c-bus", 
        type=int, 
        default=3, 
        help="I2C bus number (default: 3)"
    )
    parser.add_argument(
        "--address", 
        type=lambda x: int(x, 0), 
        default=0x08, 
        help="I2C device address in decimal or hex (default: 0x08)"
    )
    parser.add_argument(
        "--debug", 
        action="store_true", 
        help="Enable debug logging"
    )
    
    # Create subparsers for different commands
    subparsers = parser.add_subparsers(dest="command", help="Command to run")
    
    # Test sequence command
    test_parser = subparsers.add_parser("test", help="Run a test sequence")
    
    # Interactive mode command
    interactive_parser = subparsers.add_parser("interactive", help="Start interactive control mode")
    
    # Direct command parser
    direct_parser = subparsers.add_parser("direct", help="Send a direct command")
    direct_parser.add_argument(
        "action", 
        choices=["forward", "backward", "left", "right", "stop", "0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "status"],
        help="The command to send"
    )
    
    # Parse arguments
    args = parser.parse_args()
    
    # Set up logging
    setup_logging(level=logging.DEBUG if args.debug else logging.INFO)
    
    # Execute the appropriate command
    if args.command == "test":
        run_test_sequence(i2c_bus=args.i2c_bus, address=args.address)
    elif args.command == "interactive":
        interactive_mode(i2c_bus=args.i2c_bus, address=args.address)
    elif args.command == "direct":
        direct_command(args.action, i2c_bus=args.i2c_bus, address=args.address)
    else:
        # Default to interactive mode if no command specified
        print("\nZenBot-Pi Motor Controller")
        print("1. Run test sequence")
        print("2. Start interactive mode")
        choice = input("Select an option (1/2): ").strip()
       
        if choice == '1':
            run_test_sequence(i2c_bus=args.i2c_bus, address=args.address)
        elif choice == '2':
            interactive_mode(i2c_bus=args.i2c_bus, address=args.address)
        else:
            print("Invalid choice")

if __name__ == "__main__":
    main() 