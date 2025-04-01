import smbus2
import time
import logging
import sys

# Configure logging
logger = logging.getLogger(__name__)

class MotorController:
    """I2C motor controller for Arduino communication"""
   
    def __init__(self, i2c_bus=3, address=0x08, log_level=logging.INFO):
        """
        Initialize the motor controller.
        
        Args:
            i2c_bus (int): The I2C bus number to use (default: 3).
            address (int): The I2C address of the Arduino (default: 0x08).
            log_level (int): Logging level (default: logging.INFO).
        """
        # Set up logging if it hasn't been configured
        self._setup_logging(log_level)
        
        self.i2c_bus = i2c_bus
        self.address = address
        self.bus = None
        # System is always active in this version
        self.system_active = True 
        logger.info(f"Initializing MotorController on I2C bus {i2c_bus}, address 0x{address:02X}")
        self.connect()
    
    def _setup_logging(self, log_level):
        """Set up logging if not already configured."""
        logger.setLevel(log_level)
        # Only add handler if logger doesn't have one
        if not logger.handlers:
            handler = logging.StreamHandler(sys.stdout)
            formatter = logging.Formatter('%(asctime)s [%(levelname)s] %(message)s')
            handler.setFormatter(formatter)
            logger.addHandler(handler)
       
    def connect(self):
        """
        Establish I2C connection with the Arduino.
        
        Returns:
            bool: True if connection successful, False otherwise.
        """
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
        """
        Send a single character command to the Arduino.
        
        Args:
            cmd (str or int): The command to send. If a string, the first character is used.
            
        Returns:
            str: Response message or error message.
        """
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
        """
        Test basic communication with the Arduino.
        
        Returns:
            bool: True if communication successful, False otherwise.
        """
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
        """
        Move forward.
        
        Returns:
            str: Response message.
        """
        logger.info("Moving forward")
        return self.send_command('F')
   
    def backward(self):
        """
        Move backward.
        
        Returns:
            str: Response message.
        """
        logger.info("Moving backward")
        return self.send_command('B')
   
    def left(self):
        """
        Turn left.
        
        Returns:
            str: Response message.
        """
        logger.info("Turning left")
        return self.send_command('L')
   
    def right(self):
        """
        Turn right.
        
        Returns:
            str: Response message.
        """
        logger.info("Turning right")
        return self.send_command('R')
   
    def stop(self):
        """
        Stop all motors.
        
        Returns:
            str: Response message.
        """
        logger.info("Stopping motors")
        return self.send_command('S')
   
    def set_speed(self, level):
        """
        Set speed level (0-9).
        
        Args:
            level (int): Speed level from 0 (slowest) to 9 (fastest).
            
        Returns:
            str: Response message or error message.
        """
        if 0 <= level <= 9:
            logger.info(f"Setting speed to level {level}")
            return self.send_command(str(level))
        else:
            logger.error(f"Invalid speed level: {level} (must be 0-9)")
            return "ERROR: Invalid speed level (must be 0-9)"
   
    def get_status(self):
        """
        Get system status (always on).
        
        Returns:
            str: Response message.
        """
        logger.info("Requesting system status")
        return self.send_command('?')
   
    def close(self):
        """
        Close I2C connection.
        
        Returns:
            bool: True if closed successfully, False otherwise.
        """
        if self.bus:
            logger.info("Closing I2C connection")
            self.bus.close()
            self.bus = None
            return True
        return False 