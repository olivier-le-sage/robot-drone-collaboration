#!/usr/bin/env python3

# MQTT methods for sending data to particular topics
# --> see JSON message definitions for payload structures
# --> see documentation for topic hierarchy

import paho.mqtt.client as mqtt
import datetime
import sys
import json

DEFAULT_PORT = 1883 # default port for MQTT broker

class MQTTSender:

    def __init__(self, broker="", hostname="", sub_topics=[], pub_topics=[],
                QoS_level=1):
        self.broker = broker # Broker name not yet known
        self.hostname = hostname # Hostname of the PC hosting the broker on the network
        self.sub_topics = sub_topics
        self.pub_topics = pub_topics

        # Automatically subscribed to any topics passed to sub_topics
        for topic in sub_topics:
            self.subscribe(topic) # warning: not sure if this will work

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
        #     delivery of the message.
        self.QoS_level = QoS_level

        # set up the Client
        self.client = mqtt.Client('Garbage Collector')

    # callback for when the client receives a CONNACK response from the server.
    def on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            print("Connection accepted.")
        else:
            print("Connection failed: result code "+str(rc))
        pass

    def on_message(self, client, userdata, msg):
        print("RECEIVED: {" + msg.payload + "} to topic {" + msg.topic + "}")
        pass

    def on_publish(self, client, userdata, result):
        print("PUBLISHED: {" + payload + "} to topic {" + topic + "}")
        print("Payload had a length of: " + len(payload))
        pass

    def publish(self, topic, payload):
        # publish the desired message (WIP)
        self.client.publish(topic, bytes(payload, 'utf-8'), self.QoS_level)
        self.pub_topics.append(topic)
        pass

    def subscribe(self, topic):
        # subscribe to a specific topic
        self.client.subscribe(topic, self.QoS_level)
        self.sub_topics.append(topic)
        pass

    def run(self):
        self.client.on_connect = self.on_connect # function pointers
        self.client.on_publish = self.on_publish
        self.client.on_message = self.on_message

        # we connect asynchronously so that loop_start() will attempt to
        # re-connect in the event of a connection failure
        self.client.connect_async(self.broker, DEFAULT_PORT, 60)

        # Processes network traffic, dispatches callbacks and
        # handles reconnecting.
        # Other loop*() functions are available that give a threaded interface and a
        # manual interface.
        self.client.loop_start() # starts a thread, non-blocking
