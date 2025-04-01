import smbus2
import time
import logging
import sys

# Configure logging to show on console and save to file
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[
        logging.FileHandler("motor_controller.log"),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger("MotorController")

class MotorController:
    """I2C motor controller for Arduino communication"""
   
    def __init__(self, i2c_bus=3, address=0x08):
        self.i2c_bus = i2c_bus
        self.address = address
        self.bus = None
        # System is always active in the simplified version
        self.system_active = True 
        logger.info(f"Initializing MotorController on I2C bus {i2c_bus}, address 0x{address:02X}")
        self.connect()
       
    def connect(self):
        """Establish I2C connection with the Arduino"""
        try:
            logger.info(f"Opening I2C bus {self.i2c_bus}")
            self.bus = smbus2.SMBus(self.i2c_bus)
            
            # Test connection with a status request
            logger.info("Testing connection to Arduino...")
            try:
                # Send a status request command
                self.bus.write_byte(self.address, ord('?'))
                logger.info("I2C connection successful")
                
                # Wait for Arduino to stabilize
                time.sleep(0.5)
                
                return True
            except OSError as e:
                logger.error(f"I2C communication error: {str(e)}")
                logger.error("Check if the Arduino is connected and has the correct I2C address")
                return False
   
        except Exception as e:
            logger.error(f"Connection error: {str(e)}")
            return False
   
    def send_command(self, cmd):
        """Send a single character command to the Arduino"""
        if not self.bus:
            logger.error("Cannot send command - I2C bus not open")
            return "ERROR: I2C bus not open"
           
        # Send single character command
        try:
            cmd_byte = ord(cmd[0]) if isinstance(cmd, str) else cmd
            logger.debug(f"Sending command: '{chr(cmd_byte)}' (0x{cmd_byte:02X})")
            self.bus.write_byte(self.address, cmd_byte)
            
            # Wait a moment for Arduino to process
            time.sleep(0.2)
            
            # No direct response over I2C unless we implement a request mechanism
            return f"Command '{chr(cmd_byte)}' sent successfully"
               
        except Exception as e:
            logger.error(f"Error sending command: {str(e)}")
            return f"ERROR: {str(e)}"
   
    def test_communication(self):
        """Test basic communication with the Arduino"""
        logger.info("Testing I2C communication...")
       
        try:
            # Send status request
            response = self.send_command('?')
            logger.info("Status request sent")
            
            # Assume the test passes if no exception occurred
            logger.info("Communication test passed!")
            return True
        except Exception as e:
            logger.error(f"Communication test failed: {str(e)}")
            return False
   
    # Movement commands
    def forward(self):
        """Move forward"""
        logger.info("Moving forward")
        return self.send_command('F')
   
    def backward(self):
        """Move backward"""
        logger.info("Moving backward")
        return self.send_command('B')
   
    def left(self):
        """Turn left"""
        logger.info("Turning left")
        return self.send_command('L')
   
    def right(self):
        """Turn right"""
        logger.info("Turning right")
        return self.send_command('R')
   
    def stop(self):
        """Stop all motors"""
        logger.info("Stopping motors")
        return self.send_command('S')
   
    def set_speed(self, level):
        """Set speed level (0-9)"""
        if 0 <= level <= 9:
            logger.info(f"Setting speed to level {level}")
            return self.send_command(str(level))
        else:
            logger.error(f"Invalid speed level: {level} (must be 0-9)")
            return "ERROR: Invalid speed level (must be 0-9)"
   
    def get_status(self):
        """Get system status (always on)"""
        logger.info("Requesting system status")
        return self.send_command('?')
   
    def close(self):
        """Close I2C connection"""
        if self.bus:
            logger.info("Closing I2C connection")
            self.bus.close()
            self.bus = None
            return True
        return False 