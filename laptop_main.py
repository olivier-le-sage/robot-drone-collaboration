#!/usr/bin/python3

# Laptop code -- the brain of the system
#
# Runs trash detection, manages MQTT, and manages overall cohesion between
#   the robot and the drone.
# Also responsible for running complex algorithms, such as:
#   - extracting environment mapping from drone video feed/images
#   - turning drone video feed into relevant images if necessary
#   - establishing key landmarks in images using openCV + NN
#   - identifying the robot in the picture
#   - path planning
# The outputs from these algorithms are then communicated to the robot via MQTT.


import sys
import bluetooth as bt # pybluez
import datetime as dt
from threading import Thread
import subprocess
from queue import Queue

# Add module scripts one-by-one at runtime
sys.path.insert(0, 'robot-drone-collaboration/src') # import src tree
sys.path.insert(0, 'robot-drone-collaboration/lib') # import lib tree

import src
import src.Trash_Detection.TrashDetector as trash_detect
from src.PathCode.path2cmds import *
import lib
# import lib.MQTTSN_Python.MQTTSN
#import MQTTSN # this import fails because the module isn't found
from mqtt_sender import MQTTSender
import paho.mqtt.client as mqtt
import paho.mqtt.subscribe as subscribe
import paho.mqtt.publish as publish
import proto
import proto.bin.message_defs_pb2 as message_defs_pb2
import pathlib
import time


########## Constants ##########

BLUETOOTH_SVR_NAME = "" # own name
MQTT_HOSTNAME   = "LAPTOP-KDBVI58S" # hostname/IP of computer hosting the broker
GOOGLE_BROKER   = "mqtt.googleapis.com" # Google cloud-based broker
ECLIPSE_BROKER  = "mqtt.eclipse.org" # Public Eclipse MQTT broker
ECLIPSE_BROKER2 = "iot.eclipse.org" # (Other) public Eclipse MQTT broker
SPENCER_BROKER  = "192.168.137.1"
LOCAL_BROKER    = "localhost"
MQTT_BROKER     = ECLIPSE_BROKER # provisionally working
MQTT_CLIENT_ID  = '7061fe2823fe4375bcdadfbf14f184c8' # random md5 hash


SUB_TOPICS = ['olivier-le-sage/land-robot/move',
              'olivier-le-sage/land-robot/status',
              'olivier-le-sage/land-robot/mpu6050',
              'olivier-le-sage/land-robot/ping']

QUIET_MODE = True

# Code run in video
############################################################################################


def setup_pi():
    piPhysicalAddr = 'dc-a6-32-2e-b9-a8'
    command1 = 'netsh interface ip show addresses "Local Area Connection* 12"'
    process1 = subprocess.Popen(command1, stdout=subprocess.PIPE, stderr=None, shell=True)
    output1 = process1.communicate()
    netsh = output1[0].decode("utf-8")
    netstring = netsh.split()
    ipaddr = netstring[12]

    # Takes the retrieved IP address and adds it to the "arp" command which
    # retrieves all IP addresses connected to ipaddr
    maincom = 'arp -a -N ' + ipaddr

    # Inputs the arp command into the terminal to get the list of connected
    # devices and IP addresses and then searches through them to find the
    # one associated with piPhysicalAddr (MAC address of pi)

    command2 = 'arp -a -N ' + ipaddr
    process2 = subprocess.Popen(command2, stdout=subprocess.PIPE, stderr=None, shell=True)
    output2 = process2.communicate()
    arpdecoded = output2[0].decode("utf-8")
    arpstring = arpdecoded.split()
    for i in range(len(arpstring)):
        if arpstring[i] == piPhysicalAddr:
            rtmpip = arpstring[i - 1]

###########################################################################################

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

####### Message Handling ######

def on_message(client, userdata, msg):
    print("[STATUS] %s | %s" % (msg.topic, msg.payload))


def perform_verification(rtmpip):
    images = "src/Trash_Detection/images2"  # relative to this file
    ROOT_DIR = str(pathlib.Path(__file__).parent.absolute())
    print(ROOT_DIR)

    # command3 is the terminal command that connects to the RTMP stream and
    # then captures and image from it. See onClick function for more.
    command3 = r'ffmpeg -y -i rtmp://' + rtmpip + \
               r'/live/test -vframes 1 "' + ROOT_DIR + '/src/Trash_Detection/images2/verification%03d.jpg"'
    print(command3)
    process = subprocess.Popen(command3, stdout=subprocess.PIPE, stderr=None, shell=True)
    output = process.communicate()


############ Main #############


def run_main(rtmpip):
    # Setup the automatic connection to the Pi
    #setup_pi()

    # Start the bluetooth server
    bt_t = Thread(target=bluetooth_server)
    # bt_t.start()
    # print("Bluetooth started.")

    # initialize trash detection (and load images)
    images = "src/Trash_Detection/images2"  # relative to this file
    td = trash_detect.TrashDetector(images_dir=images)

    # initialize MQTT Client
    mqtt_interface = MQTTSender(MQTT_CLIENT_ID, MQTT_BROKER, MQTT_HOSTNAME,
                                    sub_topics=SUB_TOPICS, QoS_level=2)
    # mqtt_interface.subscribe("olivier-le-sage/land-robot/move")
    # mqtt_interface.start() # run mqtt_interface as a thread

    # 1. Receive images from the drone
    # Nothing to do here as we will be loading sample images for the demo
    print("[STATUS] Receiving images from drone.")

    # 2. Process images and generate path + initial location/pose of the robot
    print("[STATUS] Processing images... please wait.")
    point_list, pose, size = td.run_single(r"C:\Users\spenc\Uni Fourth Year\Capstone\Code\robot-drone-collaboration\src\Trash_Detection\images2\demo_pic.jpg",quiet_mode=QUIET_MODE)
    print("[STATUS] Trash detection complete.")

    # 3. Convert path to instructions
    commands = gen_commands_from_path(point_list, pose, size)

    # 4. Send instructions to robot via MQTT payloads
    print("[DEBUG] Commands generated from path: \n", commands)
    to_publish = []
    for cmd in commands:
        robot_cmd = message_defs_pb2.MoveCommand()
        robot_cmd.name = cmd
        if (cmd == 'move_forward') or (cmd == 'move_backward'):
            robot_cmd.arg1 = 1 # let's say 1 sec = 10 cm
        if (cmd == 'pivot_turn_left') or (cmd == 'pivot_turn_right'):
            robot_cmd.arg1 = 1 # let's say 1 sec = 10 degrees

        #mqtt_interface.publish('olivier-le-sage/land-robot/move',
        #                        robot_cmd.SerializeToString())

        to_publish.append( ('olivier-le-sage/land-robot/move',
                            robot_cmd.SerializeToString(), 2, False) )

    # for the demo we'll just publish the whole list
    publish.multiple(to_publish, hostname=MQTT_BROKER, client_id=MQTT_CLIENT_ID)

    # Then very simple subscribe to any topics we want to (blocking call)
    #subscribe.callback(on_message, SUB_TOPICS, hostname=MQTT_BROKER)

    # TODO: This should run after the robot has sent a signal acknowledging that it has reached a 'Halt' command. For now
    #  it just runs automatically for demo purposes
    perform_verification(rtmpip)
    print("[DEBUG] Entering sleep")
    time.sleep(5)
    verification_test = td.verify_trash(r"C:\Users\spenc\Uni Fourth Year\Capstone\Code\robot-drone-collaboration\src\Trash_Detection\images2\verification001.jpg")
    if verification_test:
        print("[STATUS] Litter detected.")
    else:
        print("[STATUS] NO litter detected.")

##### Interactive demo given in February 2020 #####
def run_interactive_demo():
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
