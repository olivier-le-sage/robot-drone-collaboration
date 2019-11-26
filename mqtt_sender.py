#!/usr/bin/env python3

# MQTT methods for sending data to particular topics
# --> see JSON message definitions for payload structures
# --> see documentation for topic hierarchy

import paho.mqtt.client as mqtt
import datetime
import sys
import json

class MQTTSender:

    def __init__(self, broker="", hostname="", sub_topics=[], pub_topics=[]):
        self.broker = broker # Broker name not yet known
        self.hostname = hostname # Hostname of the PC hosting the broker on the network
        self.sub_topics = sub_topics
        self.pub_topics = pub_topics

    payload = ''

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
    QoS_level = 2

    # callback for when the client receives a CONNACK response from the server.
    def on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            print("Connection accepted.")
        else:
            print("Connection failed: result code "+str(rc))
        client.subscribe(topic)
        pass

    def on_message(self, client, userdata, msg):
        print("RECEIVED: {" + msg.payload + "} to topic {" + msg.topic + "}")
        pass

    def on_publish(self, client, userdata, result):
        print("PUBLISHED: {" + payload + "} to topic {" + topic + "}")
        print("Payload had a length of: " + len(payload))
        pass

    def run(self):
        client = mqtt.Client('Garbage Collector')
        client.on_connect = on_connect # function pointers
        client.on_publish = on_publish
        client.on_message = on_message
        client.connect(BROKER, 1883, 60)

        # publish the desired message
        # client.publish(topic, bytes(payload, 'utf-8'), QoS_level)

        # Blocking call that processes network traffic, dispatches callbacks and
        # handles reconnecting.
        # Other loop*() functions are available that give a threaded interface and a
        # manual interface.
        client.loop()
