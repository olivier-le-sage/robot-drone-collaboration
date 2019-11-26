import time
import RPi.GPIO as GPIO

#GPIO.Board: refer to the pins by their number 
GPIO.setmode(GPIO.BOARD)

#sensor pin number
pin_Sensor = 11
result= False
#counter = 0

#Setup GPIO ports or pins as input
GPIO.setup(pin_Sensor, GPIO.IN)


#while counter < 25:
try:
    while True:
         #reading input
        if GPIO.input(pin_Sensor):
            result= True
        else:
            result = False
        print("The result is :" + str(result))
   # counter = counter +1


# use Control - C to stop the loop   
except KeyboardInterrupt:
    print("Interrupt ")
    #Clean GPIO
    GPIO.cleanup()
    
