#!/usr/bin/python3

# Robot main control loop
# Accesses all sensor data, actuates all components as required
# Communicates data to bluetooth link and interprets instructions received from
#     main control system.
import sys
import datetime as dt
import socket
import time
import struct
import threading
import bluetooth as bt # bluetooth using PyBluez
import MQTTSN
from pprint import pprint

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
MQTT_HOSTNAME = '' # hostname/IP of computer hosting the broker

ROBOT_WIDTH = 0.03 # ~30 cm
ROBOT_HEIGHT = 0.03 # ~30 cm

BLUETOOTH_TGT_NAME = "Laptop" # TBD
BLUETOOTH_TGT_ADDR = None     # TBD

########## Initialization ##########

# Initialize bluetooth connection
# First we search for devices nearby and try to connect to the laptop
target_address = None
bluetooth_connected = False
nearby_devices = bt.discover_devices(duration=8) # scans for ~8 seconds
for bdaddr in nearby_devices:
    if BLUETOOTH_TGT_NAME == bt.lookup_name(bdaddr):
        target_address = bdaddr
        break

if target_address is not None:
    print("Found target bluetooth device with address ", target_address)
    bluetooth_connected = True
else:
    print("Could not find target bluetooth device nearby.")

# Next we find services on the device
# The laptop may also advertise a service for us to connect to
if target_address is not None:
    services = bt.find_service(address=target_address)
    pprint(services)

# Then, once the device has been found, we open a bluetooth socket
# sock = bt.BluetoothSocket(bt.RFCOMM)
# sock.connect((target_address, 1)) # port 1

# Set up MQTTSN Client
# Usage explained at: http://www.steves-internet-guide.com/python-mqttsn-client/
client = Client("land-robot", host=MQTT_HOSTNAME, port=1884)
client.registerCallback(Callback())
client.connect()
client.subscribe("land-robot/status")
client.publish("land-robot/status", "Bluetooth link established.", port=1884)

# initialize servo interface
servo_interface = ServoControl(LEFT_SERVO_PIN,
                               RIGHT_SERVO_PIN,
                               HEADTILT_SERVO_PIN,
                               HEADROT_SERVO_PIN)

mpu6050_interface = MPU6050Interface() # initialize acc/gyro interface
mqtt_interface = MQTTSender(MQTT_BROKER, MQTT_HOSTNAME)

client.publish("land-robot/status", "Initialization complete!", port=1884)

########## Self-Tests/Diagnostics ##########

# self-test servos
print("===== Testing servos =====")
servo_interface.test_run()

# self-test accelerometer/gyroscope by reading some values
print("===== Testing accelerometer/gyroscope =====")
print(str(dt.datetime.now()), "Accelerometer: ", mpu6050_interface.get_acc())
print(str(dt.datetime.now()), "Gyroscope: ", mpu6050_interface.get_gyr())

# self-test ultrasonic sensor (PING sensor)

# self-test GPS reading

# self-test range sensors (Sharp GPD12 IR sensors)

# self-test Camera functionality

########## Main Loop ##########

# 1. Retrieve all sensor data using sensor interfaces and C functions


# 2. Publish to MQTT-SN broker


# 3. Retrieve any instructions/data arriving on the robot's topics


# 4. Execute instructions (turn left, stop moving, process path data... etc)
# 4b. Update robot movement state if necessary (and publish it to MQTT-SN broker)

# Rinse and repeat
