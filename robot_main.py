#!/usr/bin/python3
# Main control loop
# Accesses all sensor data, actuates all components as required
# Communicates data to bluetooth link and interprets instructions received from
#     main control system.
import sys
import datetime as dt
import socket
import time
import struct
import MQTTSN, MQTTSNinternal

# Add module scripts one-by-one at runtime
sys.path.insert(0, 'robot-drone-collaboration/src') # import src tree
sys.path.insert(0, 'robot-drone-collaboration/lib') # import lib tree
#sys.path.insert(0, ...)

# import modules
from mqtt_sender import MQTTSender
import src
from src.HS_805.servos import ServoControl
from src.MPU_6050.MPU6050Interface import MPU6050Interface
import lib
import lib.MQTTSN_Python.MQTTSNclient.py

########## Constants ##########

LEFT_SERVO_PIN  = 23 # the big original servo
RIGHT_SERVO_PIN = 24 # the small replacement servo
HEADTILT_SERVO_PIN = 27 # the small replacement servo
HEADROT_SERVO_PIN = 22 # the small replacement servo
MQTT_BROKER = '' # TBD
MQTT_HOSTNAME = '' # hostname of computer hosting the broker

########## Initialization ##########

# Set up MQTTSN Client
client = Client("land-robot", port=1885)
client.registerCallback(Callback())
client.connect()

# initialize servo interface
servo_interface = ServoControl(LEFT_SERVO_PIN,
                               RIGHT_SERVO_PIN,
                               HEADTILT_SERVO_PIN,
                               HEADROT_SERVO_PIN)

mpu6050_interface = MPU6050Interface() # initialize acc/gyro interface
mqtt_interface = MQTTSender(MQTT_BROKER, MQTT_HOSTNAME)

########## Tests ##########

# Test servos
print("===== Testing servos =====")
servo_interface.test_run()

# Test accelerometer/gyroscope by reading some values
print("===== Testing accelerometer/gyroscope =====")
print(str(dt.datetime.now()), "Accelerometer: ", mpu6050_interface.get_acc())
print(str(dt.datetime.now()), "Gyroscope: ", mpu6050_interface.get_gyr())

########## Main Loop ##########

# 1. Retrieve all sensor data using sensor interfaces and C functions


# 2. Publish to MQTT-SN broker


# 3. Retrieve any instructions/data arriving on the robot's topics


# 4. Execute instructions (turn left, stop moving, process path data... etc)
# 4b. Update robot movement state if necessary (and publish it to MQTT-SN broker)

# Rinse and repeat
