#!/usr/bin/env python3
"""
Example of how to integrate controlPI with an LLM for robot control
This is just a skeleton example - you would need to add your own LLM integration
"""
import time
import re
from controlPI import MotorController

class RobotLLMController:
    """A simple class to interface between an LLM and a robot"""
    
    def __init__(self, i2c_bus=3, address=0x08):
        """Initialize the controller"""
        self.controller = MotorController(i2c_bus=i2c_bus, address=address)
        self.is_active = False
        self.last_command = None
        
        # Try to establish communication
        if not self.controller.test_communication():
            raise Exception("Failed to communicate with Arduino")
    
    def process_llm_command(self, llm_text):
        """Process natural language command from an LLM and control the robot"""
        # Convert to lowercase for easier matching
        text = llm_text.lower()
        
        # Check for system commands first
        if re.search(r'(start|activate|turn on|wake up)', text):
            if not self.is_active:
                self.controller.toggle_system()
                self.is_active = True
                return "Robot system activated"
            else:
                return "Robot is already active"
                
        if re.search(r'(stop|deactivate|turn off|shutdown|shut down)', text):
            self.controller.stop()  # Stop motors first
            if self.is_active:
                self.controller.toggle_system()
                self.is_active = False
                return "Robot system deactivated"
            else:
                return "Robot is already inactive"
        
        # If system is not active, we can't control motors
        if not self.is_active:
            return "Robot is not active. Please activate the robot first."
        
        # Process movement commands
        if re.search(r'(move|go) forward', text):
            self.controller.forward()
            self.last_command = "forward"
            return "Moving forward"
            
        if re.search(r'(move|go) backward|go back', text):
            self.controller.backward()
            self.last_command = "backward"
            return "Moving backward"
            
        if re.search(r'turn (left|to the left)', text):
            self.controller.left()
            self.last_command = "left"
            return "Turning left"
            
        if re.search(r'turn (right|to the right)', text):
            self.controller.right()
            self.last_command = "right"
            return "Turning right"
            
        if re.search(r'stop moving|halt|freeze', text):
            self.controller.stop()
            self.last_command = "stop"
            return "Stopped movement"
        
        # Speed control
        speed_match = re.search(r'(set|change) speed (to )?([\d]|max|maximum|half|medium|slow|minimum)', text)
        if speed_match:
            speed_text = speed_match.group(3)
            
            # Convert text speed to number
            speed_level = None
            if speed_text == "max" or speed_text == "maximum":
                speed_level = 9
            elif speed_text == "half" or speed_text == "medium":
                speed_level = 5
            elif speed_text == "slow" or speed_text == "minimum":
                speed_level = 1
            elif speed_text.isdigit():
                speed_level = int(speed_text)
                if speed_level > 9:
                    speed_level = 9
            
            if speed_level is not None:
                self.controller.set_speed(speed_level)
                return f"Speed set to {speed_level}"
        
        # Return status if asked
        if re.search(r'(status|what are you doing|where are you|how are you)', text):
            return f"Robot is active. Last command: {self.last_command or 'None'}"
            
        # Default response if no command matched
        return "I don't understand that command. Try simple movement commands like 'move forward' or 'turn right'."
    
    def close(self):
        """Clean up resources"""
        self.controller.stop()
        self.controller.close()


# Example usage
def demo_llm_interface():
    """Demonstrate the LLM interface with simulated commands"""
    print("Starting robot LLM controller...")
    robot = RobotLLMController()
    
    # Example commands that might come from an LLM
    example_commands = [
        "Please activate the robot system",
        "Set speed to medium",
        "Please move forward",
        "Turn to the right",
        "Move forward again",
        "Stop moving",
        "What's your status?",
        "Please shut down the robot"
    ]
    
    try:
        for cmd in example_commands:
            print(f"\nLLM Command: '{cmd}'")
            response = robot.process_llm_command(cmd)
            print(f"Robot Response: {response}")
            time.sleep(2)  # Pause between commands
            
    except KeyboardInterrupt:
        print("\nDemo interrupted!")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        robot.close()
        print("Demo completed!")

if __name__ == "__main__":
    print("Robot LLM Integration Demo")
    print("=========================")
    demo_llm_interface() 