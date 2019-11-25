#!/usr/bin/python3
# Main control loop
# Accesses all sensor data, actuates all components as required
# Communicates data to bluetooth link and interprets instructions received from
#     main control system.
import sys

# Add module scripts one-by-one at runtime
sys.path.append('/src/HS_805/servos.py')
#sys.path.append(...)

########## Constants ##########

LEFT_SERVO_PIN  = 23
RIGHT_SERVO_PIN = 24

########## Initialization ##########

servo_interface = ServoControl(LEFT_SERVO_PIN, RIGHT_SERVO_PIN)
servo_interface.test_run()

########## Loop ##########

# 1. Retrieve all sensor data using sensor interfaces and C functions


# 2. Publish to MQTT-SN broker


# 3. Retrieve any instructions/data arriving on the robot's topics


# 4. Execute instructions (turn left, stop moving, process path data... etc)

# Rinse and repeat
