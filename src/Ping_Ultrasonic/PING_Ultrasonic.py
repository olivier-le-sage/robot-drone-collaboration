#!/usr/bin/python3
# PING Ultrasonic echolocation distance sensor code. Based on:
# https://www.element14.com/community/community/stem-academy/blog/2014/12/21/ping-me
import time
import datetime as dt
import RPi.GPIO as GPIO
from queue import Queue

# Due to its time-sensitive nature we run this sensor in its own thread
# Because of this, a certain amount of inaccuracy is expected

# Pin numberings are BOARD-mode
GPIO.setmode(GPIO.BOARD) # this may trigger a "mode already set" warning

class Ultrasonic(Thread):
    def __init__(self, trig_pin, period=1):
        # Call thread superclass constructor
        super(Ultrasonic, self).__init__()

        self.ctrl_pin = trig_pin
        self.period = period # gives the delay (in s) between pings when running
        self.ping_q = Queue()

    def single_test(self):
        ''' Single test of the PING distance sensor. Returns -1 on failure. '''

        distance = -1
        print("Testing ultrasonic sensor on pin ", str(self.trig_pin))
        distance = self.read_distance()
        print("Distance to object is ",distance," cm or ",distance*.3937," inches")
        return distance

    def read_distance(self):
       GPIO.setup(self.trig_pin, GPIO.OUT)
       GPIO.output(self.trig_pin), 0)
       time.sleep(0.000002)

       #send trigger signal
       GPIO.output(self.trig_pin, 1)

       time.sleep(0.000005)

       GPIO.output(self.trig_pin, 0)

       GPIO.setup(self.trig_pin, GPIO.IN)


       while GPIO.input(pin)==0:
          starttime=time.time()

       while GPIO.input(pin)==1:
          endtime=time.time()

       duration=endtime-starttime
       # Distance is defined as time/2 (there and back) * speed of sound 34000 cm/s
       distance=duration*34000/2
       return distance

    def run(self):
        '''
            A thread implementation that simply pings periodically
        '''

        while True:
            dist = self.read_distance()
            timestamp = str(dt.datetime.now())
            self.ping_q.put((dist, timestamp))
            sleep(self.period)
