#!/usr/bin/python3

# Laptop code -- the brain of the system
#
# Runs a bluetooth server, manages MQTT, and manages overall cohesion between
#   the robot and the drone.
# Also responsible for running complex algorithms, such as:
#   - extracting environment mapping from drone video
#   - turning drone video into relevant images
#   - establishing key landmarks in images using openCV
#   - path planning
# The outputs from these algorithms are then communicated to the robot via MQTT.

import sys
import bluetooth as bt
import datetime as dt
from threading import Thread
from queue import Queue

# Add module scripts one-by-one at runtime
sys.path.insert(0, 'robot-drone-collaboration/src') # import src tree
sys.path.insert(0, 'robot-drone-collaboration/lib') # import lib tree

import lib
# import lib.MQTTSN_Python.MQTTSN
#import MQTTSN # this import fails because the module isn't found
from mqtt_sender import MQTTSender
import paho.mqtt.client as mqtt
import proto
import proto.bin.message_defs_pb2 as message_defs_pb2

########## Constants ##########

BLUETOOTH_SVR_NAME = "" # own name
MQTT_HOSTNAME   = "LAPTOP-KDBVI58S" # hostname/IP of computer hosting the broker
GOOGLE_BROKER   = "mqtt.googleapis.com" # Google cloud-based broker
ECLIPSE_BROKER  = "mqtt.eclipse.org" # Public Eclipse MQTT broker
ECLIPSE_BROKER2 = "iot.eclipse.org" # (Other) public Eclipse MQTT broker
SPENCER_BROKER  = "192.168.137.1"
LOCAL_BROKER    = "localhost"
MQTT_BROKER     = LOCAL_BROKER # provisionally working
MQTT_CLIENT_ID  = '7061fe2823fe4375bcdadfbf14f184c8' # random md5 hash

SUB_TOPICS = ['olivier-le-sage/land-robot/move']

####### Bluetooth server ######

def bluetooth_server():
    ''' Runs bluetooth-related code on a separate thread. '''

    # Create a socket and listen to it
    sock = bt.BluetoothSocket(bt.RFCOMM)
    sock.bind( (BLUETOOTH_SVR_NAME, 30) )
    sock.listen(1) # listen to accept 1 connection at a time

    # accept a connection
    conn, addr = sock.accept()
    print("Connection accepted with ", addr)

    # Receive data on that connection
    while True:
        data = conn.recv(1024) # A max of 1024 bytes at a time
        print(data) # for now we simply print
        # in the future we will also manipulate the data

############ Main #############

# Start the bluetooth server
bt_t = Thread(target=bluetooth_server)
# bt_t.start()
print("Bluetooth started.")

# initialize MQTT Client
mqtt_interface = MQTTSender(MQTT_CLIENT_ID, MQTT_BROKER, MQTT_HOSTNAME,
                                sub_topics=SUB_TOPICS)
# mqtt_interface.subscribe("olivier-le-sage/land-robot/move")
mqtt_interface.start() # run mqtt_interface as a thread

# For now we'll keep it simple -- a while loop where the user decides which
#     command to send to the robot
print("Instructions: Enter a number to give the robot a preconfigured command.")
print("1 - Move forward for 5 seconds.")
print("2 - Move backward for 5 seconds.") # For now this goes forward (WIP)
print("3 - Turn left.")
print("4 - Turn right.")
print("5 - Neutral (stop).")
while True:

    # Check for any messages received
    if not mqtt_interface.message_q.empty():
        print("There's a message in the queue! Received: ",str(message_q.get()))

    command = input("Enter command: ")
    if command == "1":
        robot_cmd = message_defs_pb2.MoveCommand()
        robot_cmd.name = 'move_forward'
        robot_cmd.arg1 = 5
        mqtt_interface.publish('olivier-le-sage/land-robot/move',
                                robot_cmd.SerializeToString())
        print("move() command sent.")
    elif command == "2":
        robot_cmd = message_defs_pb2.MoveCommand()
        robot_cmd.name = 'move_backward'
        robot_cmd.arg1 = 5
        mqtt_interface.publish('olivier-le-sage/land-robot/move',
                                robot_cmd.SerializeToString())
        print("move() command sent.")
    elif command == "3":
        robot_cmd = message_defs_pb2.MoveCommand()
        robot_cmd.name = 'pivot_turn_left'
        robot_cmd.arg1 = 5
        mqtt_interface.publish('olivier-le-sage/land-robot/move',
                                robot_cmd.SerializeToString())
        print("pivot_turn_left() command sent.")
    elif command == "4":
        robot_cmd = message_defs_pb2.MoveCommand()
        robot_cmd.name = 'pivot_turn_right'
        robot_cmd.arg1 = 5
        mqtt_interface.publish('olivier-le-sage/land-robot/move',
                                robot_cmd.SerializeToString())
        print("pivot_turn_right() command sent.")
    elif command == "5":
        robot_cmd = message_defs_pb2.MoveCommand()
        robot_cmd.name = 'neutral'
        mqtt_interface.publish('olivier-le-sage/land-robot/move',
                                robot_cmd.SerializeToString())
        print("pivot_turn_right() command sent.")
    else:
        print("ERROR: Invalid input. Try again.")
