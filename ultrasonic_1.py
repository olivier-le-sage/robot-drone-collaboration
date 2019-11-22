#!/usr/bin/python3
# ultrasonic_1.py
# Measure distance using an ultrasonic module

# Import required Python libraries
import time
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM) # broadcom pin numbering
GPIO.setwarnings(False) # not sure what this does yet
timeout = 0.020

# Define GPIO to use on Pi
GPIO_SIG = 18
NUM_READS = 5

print("Ultrasonic Measurement Test Program")
i = 0
while i < NUM_READS:


    # Set signal pin as output
    GPIO.setup(GPIO_SIG, GPIO.OUT)  # Signal

    # Send signal
    GPIO.output(GPIO_SIG, 1)

    # Allow module to settle
    time.sleep(0.5)

    # Now setup as input
    GPIO.setup(GPIO_SIG, GPIO.IN)

    goodread = True
    watchtime = time.time()
    while GPIO.input(GPIO_SIG) == 0 and goodread:
        starttime = time.time()
        if (starttime - watchtime > timeout):
            goodread = False

    if goodread:
        watchtime = time.time()
        while GPIO.input(GPIO_SIG) == 1 and goodread:
            endtime = time.time()
            if (endtime - watchtime > timeout):
                goodread = False

    if goodread:
        # Calculate pulse length
        duration = endtime - starttime

        # Distance pulse travelled in that time is time
        # multiplied by the speed of sound (cm/s)
        # That was the distance there and back so halve the value
        distance = duration * 34000 / 2
        print("Distance : ", distance)
        i += 1

# Reset GPIO settings
GPIO.cleanup()
