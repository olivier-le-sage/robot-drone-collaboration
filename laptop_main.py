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
import MQTTSN

########## Constants ##########

BLUETOOTH_SVR_NAME = "Laptop" # own name

####### Bluetooth server ######

def bluetooth_server():
    ''' Runs bluetooth-related code on a separate thread. '''

    # Create a socket and listen to it
    sock = BluetoothSocket(bt.RFCOMM)
    sock.bind( (BLUETOOTH_SVR_NAME, 1) )
    sock.listen(1) # listen to accept 1 connection at a time

    # accept a connection
    conn, addr = sock.accept()
    print("Connection accepted with ", addr)

    # Receive data on that connection
    while True:
        data = conn.recv(1024) # A max of 1024 bytes at a time
        print(data) # for now we simply print
        # in the future we will also

############ Main #############

# Start the bluetooth server
print("Starting bluetooth...")
bt_t = Thread(target=bluetooth_server)
bt_t.start()
