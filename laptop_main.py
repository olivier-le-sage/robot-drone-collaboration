#!/usr/bin/python3

# Laptop code
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
import lib.MQTTSN_Python.MQTTSN
#import MQTTSN # this import fails because the module isn't found

########## Constants ##########

BLUETOOTH_SVR_NAME = "" # own name

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
bt_t.start()
print("Bluetooth started.")
