#!/usr/bin/python3
# Main control loop
# Accesses all sensor data, actuates all components as required
# Communicates data to bluetooth link and interprets instructions received from
#     main control system.
import sys

# Add module scripts one-by-one at runtime
#sys.path.insert(0, '/src/HS_805/servos.py')
#sys.path.insert(0, ...)

# import modules
from src.HS_805.servos import ServoControl

########## Constants ##########

LEFT_SERVO_PIN  = 23 # the big original servo
RIGHT_SERVO_PIN = 24 # the small replacement servo

########## Initialization ##########

servo_interface = ServoControl(LEFT_SERVO_PIN, RIGHT_SERVO_PIN)
servo_interface.test_run()

########## Loop ##########

# 1. Retrieve all sensor data using sensor interfaces and C functions


# 2. Publish to MQTT-SN broker


# 3. Retrieve any instructions/data arriving on the robot's topics


# 4. Execute instructions (turn left, stop moving, process path data... etc)

# Rinse and repeat
