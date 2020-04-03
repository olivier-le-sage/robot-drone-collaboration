#!/usr/bin/env python3

# MQTT methods for sending data to particular topics
# --> see JSON message definitions for payload structures
# --> see documentation for topic hierarchy

import paho.mqtt.client as mqtt
import datetime
import sys
import json
from queue import Queue
from threading import Thread

DEFAULT_PORT = 1883 # default port for MQTT broker
GOOGLE_PORT  = 8883 # default port for Google's cloud-based MQTT API
GOOGLE_ALT_PORT = 443 # alternative port for Google's MQTT API

class MQTTSender(Thread):

    def __init__(self, clientID, broker="", hostname="", sub_topics=[],
                pub_topics=[], QoS_level=1):

        # Call Thread superclass init()
        super(MQTTSender, self).__init__()

        self.broker = broker # Broker name not yet known
        self.hostname = hostname # Hostname of the PC hosting the broker on the network
        self.sub_topics = sub_topics
        self.pub_topics = pub_topics
        self.message_q = Queue() # used to fetch messages in sync

        ##### Quality-of-Service level #####
        # There are three QoS levels. They represent the complexity of handshaking
        # between a client and the broker. QoS 2 is the slowest, but also the most
        # reliable.
        #
        # * QoS 0: The client sends the message with minimal handshaking. There's no way
        #     to know if messages were received or not.
        # * QoS 1: The client sends and re-sends the message until an acknowledgment is
        #     received from the broker. Multiple copies of the message may arrive.
        # * QoS 2: The client and broker perform a four-way handshake to guarantee
        #     delivery of exactly one message copy.
        self.QoS_level = QoS_level

        # set up the Client
        self.client = mqtt.Client(clientID)
        self.client.on_log = self.on_log
        self.client.on_connect = self.on_connect
        self.client.on_publish = self.on_publish
        self.client.on_message = self.on_message
        self.client.on_subscribe = self.on_subscribe

        # we connect asynchronously so that loop_start() will attempt to
        # re-connect in the event of a connection failure
        self.client.connect(self.broker, DEFAULT_PORT, 60)

    # callback for when the client receives a CONNACK response from the server.
    def on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            print("[STATUS] MQTT Connection accepted.")
        else:
            print("[ERROR] MQTT Connection failed: result code "+str(rc))

        for topic in self.sub_topics:
            self.client.subscribe(topic, qos=self.QoS_level)

    def on_message(self, client, userdata, message):
        msg = message
        print("RECEIVED: {" + msg.payload + "} to topic {" + msg.topic + "}")
        self.message_q.put((msg.topic, msg.payload))

    def on_publish(self, client, userdata, mid):
        print("PUBLISHED: {" + payload + "} to topic {" + topic + "}")
        print("Payload had a length of: " + len(payload))

    def on_subscribe(self, client, userdata, mid, granted_qos):
        print("SUBSCRIBED successfully with QoS ", str(granted_qos))

    # DEBUG CALLBACK
    def on_log(client, userdata, level, buf):
        print("[LOG lvl", str(level), "] ", str(buf))

    def publish(self, topic, payload):
        # publish the desired message (WIP)
        self.client.publish(topic, payload=payload, qos=self.QoS_level)
        self.pub_topics.append(topic)

    def subscribe(self, topic):
        # subscribe to a specific topic
        self.client.subscribe(topic, qos=self.QoS_level)
        if topic not in self.sub_topics:
            self.sub_topics.append(topic)

    def run(self):
        '''
            Start the MQTT client.
        '''
        # Processes network traffic, dispatches callbacks and
        # handles reconnecting.
        # Other loop*() functions are available that give a threaded interface and a
        # manual interface.

        #self.client.loop_start() # starts a thread, non-blocking
        self.client.loop_forever() # blocking call (never returns)
