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
from pprint import pprint
# import MQTTSN

# Add module scripts one-by-one at runtime
sys.path.insert(0, 'robot-drone-collaboration/src') # import src tree
sys.path.insert(0, 'robot-drone-collaboration/lib') # import lib tree
sys.path.insert(0, 'robot-drone-collaboratin/proto') # import proto tree
#sys.path.insert(0, ...)

# import modules
from mqtt_sender import MQTTSender
import src
from src.HS_805.servos import ServoControl
from src.MPU_6050.MPU6050Interface import MPU6050Interface
import src.Ping_Ultrasonic.PING_Ultrasonic as ping
import lib
# import lib.MQTTSN_Python.MQTTSNclient.py
import proto
import proto.bin.message_defs_pb2 as message_defs_pb2


########## Constants ##########

# BOARD-mode pin numbers
LEFT_SERVO_PIN  = 12 # the big original servo
RIGHT_SERVO_PIN = 33 # the small replacement servo
# HEADTILT_SERVO_PIN = 13 # the small replacement servo
# HEADROT_SERVO_PIN = 15 # the small replacement servo
HEADTILT_SERVO_PIN = 27
HEADROT_SERVO_PIN  = 22
PING_TRIG_PIN = 11 # or GPIO17 in BCM mode

## MQTT-related constants
# public brokers: https://github.com/mqtt/mqtt.github.io/wiki/public_brokers
MQTT_HOSTNAME   = 'LAPTOP-KDBVI58S' # hostname/IP of computer hosting the broker
GOOGLE_BROKER   = "mqtt.googleapis.com" # Google cloud-based broker
ECLIPSE_BROKER  = "mqtt.eclipse.org" # Public Eclipse MQTT broker
ECLIPSE_BROKER2 = "iot.eclipse.org" # (Other) public Eclipse MQTT broker
SPENCER_BROKER  = "192.168.137.1" # IP of the local broker on Spencer's computer
LOCAL_BROKER    = "localhost"
MQTT_BROKER     = LOCAL_BROKER # provisionally working
MQTT_CLIENT_ID  = '9de151a4906d46f5beacb41d86e036a2' # random md5 hash
MQTT_CLIENT_ID2 = '9de151a4906d46f5ceacb41d96e036a3' # random md5 hash
sub_topics = ["olivier-le-sage/land-robot/#"]


ROBOT_WIDTH = 0.03 # ~30 cm
ROBOT_HEIGHT = 0.03 # ~30 cm

BLUETOOTH_TGT_NAME = 'LAPTOP-KDBVI58S' # TBD
BLUETOOTH_TGT_ADDR = None # TBD

########## Initialization ##########

# Initialize bluetooth connection
# First we search for devices nearby and try to connect to the laptop
target_address = None
bluetooth_connected = False
nearby_devices = bt.discover_devices(duration=1) # scans for ~8 seconds
for bdaddr in nearby_devices:
    print("Bluetooth device found: " + str(bdaddr) + " "
		+ str(bt.lookup_name(bdaddr)))
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
#client = Client("land-robot", host=MQTT_HOSTNAME, port=1884)
#client.registerCallback(Callback())
#client.connect()
#client.subscribe("land-robot/status")
#client.publish("land-robot/status", "Bluetooth link established.", port=1884)

# initialize servo interface
servo_interface = ServoControl(LEFT_SERVO_PIN,
                               RIGHT_SERVO_PIN,
                               HEADTILT_SERVO_PIN,
                               HEADROT_SERVO_PIN)

mpu6050_interface = MPU6050Interface() # initialize acc/gyro interface
ping_interface = ping.Ultrasonic(PING_TRIG_PIN) # initialize PING sensor interface
mqtt_interface = MQTTSender(MQTT_CLIENT_ID, MQTT_BROKER, MQTT_HOSTNAME)
mqtt_interface.start() # start mqtt client thread in bg

##### Feb 25 Demo temporary code ###########

def on_publish(client, userdata, mid):
    print("PUBLISHED")
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("[STATUS] MQTT Connection accepted.")
    else:
        print("[ERROR] MQTT Connection failed: result code "+str(rc))

def on_subscribe(client, userdata, mid, granted_qos):
    print("SUBSCRIBED successfully")
def on_message(client, userdata, message):
    print("RECEIVED a message on ", message.topic)
def interpret_command(client, userdata, message):
    '''Callback for messages received on olivier-le-sage/land-robot/move'''

    # DEBUG message
    print("INTERPRETING message received on olivier-le-sage/land-robot/move!")

    # pass the payload to the servo interface
    move_cmd = message_defs_pb2.MoveCommand()
    move_cmd.ParseFromString(message.payload)
    servo_interface.cmd_q.put((move_cmd.name, move_cmd.arg1, move_cmd.arg2))

# Temporary client for the demo
mqttc = mqtt.Client(MQTT_CLIENT_ID2)
mqttc.on_publish = on_publish
mqttc.on_connect = on_connect
mqttc.on_subscribe = on_subscribe
mqttc.message_callback_add('olivier-le-sage/land-robot/move', interpret_command)
mqttc.connect(MQTT_BROKER, 1883, 60)
mqttc.loop_start()

########## Self-Tests/Diagnostics ##########

# self-test servos
print("===== Testing servos =====")
servo_interface.test_run()

# self-test accelerometer/gyroscope by reading some values
print("===== Testing accelerometer/gyroscope =====")
print(str(dt.datetime.now()),"Accelerometer: ", mpu6050_interface.get_acc_xyz())
print(str(dt.datetime.now()),"Gyroscope: ", mpu6050_interface.get_gyr_xyz())

# self-test MQTT interface
print("===== Testing MQTT pub-sub =====")
mqtt_interface.subscribe("olivier-le-sage/land-robot/#")
mqtt_interface.publish("olivier-le-sage/land-robot/status",
                            "Initialization complete!")

# self-test ultrasonic sensor (PING sensor)
print("===== Testing PING sensor =====")
ping_interface.single_test()

# self-test GPS reading

# self-test range sensors (Sharp GPD12 IR sensors)

# self-test Camera functionality

########## Threads ##########

# start servo interface thread
servo_interface.start() # will invoke run() in a separate thread

# start ultrasonic ping sensor thread
ping_interface.start()

########## Main Loop ##########

while True:

    # 1. Retrieve all sensor data using sensor interfaces and C functions

    # retrieve acc/gyro data
    mpu6050_data = message_defs_pb2.MPU6050Data()
    mpu6050_data.Ax, mpu6050_data.Ay, mpu6050_data.Az = mpu6050_interface.get_acc_xyz()
    mpu6050_data.Gx, mpu6050_data.Gy, mpu6050_data.Gz = mpu6050_interface.get_gyr_xyz()
    mpu6050_data.timestamp = str(dt.datetime.now())

    # retrieve ping sensor data
    ping_payload = None
    if not ping_interface.ping_q.empty():
        ping_data = message_defs_pb2.PINGDistance()
        ping_data.dist, ping_data.timestamp = ping_interface.ping_q.get()
        ping_payload = ping_data.SerializeToString()

    # 2. Publish to MQTT broker
    mpu6050_payload = mpu6050_data.SerializeToString()
    # print("Compiled protobuf payload for mpu6050: ", mpu6050_payload) # DEBUG
    mqtt_interface.publish("olivier-le-sage/land-robot/mpu6050", mpu6050_payload)
    if ping_payload is not None:
        mqtt_interface.publish("olivier-le-sage/land-robot/ping", ping_payload)

    # 3. Retrieve any instructions/data arriving on the robot's topics

    # retrieve from mqtt interface message Queue
    if not mqtt_interface.message_q.empty():
        instr = mqtt_interface.message_q.get()

        # if the topic is the servo topic, pass the payload to the servo interf
        if instr[0] == 'olivier-le-sage/land-robot/move':
            move_cmd = message_defs_pb2.MoveCommand()
            move_cmd.ParseFromString(instr[1])
            servo_interface.cmd_q.put((move_cmd.name, move_cmd.arg1, move_cmd.arg2))

        # other topics will have different behaviour (WIP)

    # 4. Execute instructions (turn left, stop moving, process path data... etc)
    # 4b. Update robot movement state if necessary (and publish it to MQTT-SN broker)

    # Rinse and repeat
    time.sleep(1) # For demo purposes we'll insert a second here to avoid flooding
