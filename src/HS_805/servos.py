from gpiozero import Servo
from time import sleep

servo = Servo(17)

print("Program for making a GPIO blink")

while True:
    servo.min()
    sleep(2)
    servo.mid()
    sleep(2)
    servo.max()
    sleep(2)
