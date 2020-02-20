# High-level servo control & optical encoder read routines.

from gpiozero import Servo
from gpiozero import AngularServo
import RPi.GPIO as GPIO
from time import sleep

# set GPIO mode to BCM (NB: not the physical pin numbers)
GPIO.setmode(GPIO.BOARD)

# PWM-capable GPIOs (two GPIOs per PWM) on the RPi 4
PWM0_PIN = 12 # 32 # BOARD-mode pins
PWM1_PIN = 33 # ?? # BOARD-mode pins

# Servo duty cycle characteristics. Vary by manufacturer.
# Futaba S148 -- goes COUNTER-CLKWISE with increasing DC
FUT_DC_MIN = 2.75  # 550 usec @50Hz
FUT_DC_MAX = 11.65 # 2330 usec @50Hz
# FUT_DC_NEUT = (FUT_DC_MIN + FUT_DC_MAX) / 2 # assumed to be the middle
FUT_DC_NEUT = 7.6 # 1520 usec @50Hz (skeptical)

# HS-805 -- goes CLKWISE with increasing DC
# 400 usec DC difference <==> 45 degrees
HS_DC_MIN = 3.5  # 1500-400*2 = 700  usec @50Hz
HS_DC_MAX = 11.5 # 1500+400*2 = 2300 usec @50Hz
HS_DC_NEUT = 7.5 # 1500 usec @50Hz

# The two different servos have different duty cycle requirements
RIGHT_DC = FUT_DC_NEUT
LEFT_DC  = HS_DC_NEUT

# RPi PWM clock base frequency
RPI_PWM_BASE_FREQ = 19.2e6

LEFT_ENCODER    = 0
RIGHT_ENCODER   = 1
LEFT_SERVO      = 0
RIGHT_SERVO     = 1

class ServoControl:
    '''
        Servo control interface.
        Provides access to high-level servo control methods.
    '''

    def __init__(self, left_servo_pin=18,
                       right_servo_pin=13,
                       headtilt_servo_pin=27,
                       headrot_servo_pin=22):

        # NB: Default pin settings are BCM-mode.
        #       physically they're (resp.) 12, 33, 13, 15
        # self.left_servo  = AngularServo(left_servo_pin, min_angle=-90, max_angle=90)
        # self.right_servo = AngularServo(right_servo_pin, min_angle=-90, max_angle=90)
        # self.headtilt_servo = AngularServo(headtilt_servo_pin, min_angle=-90, max_angle=90)
        # self.headrot_servo = AngularServo(headrot_servo_pin, min_angle=-90, max_angle=90)

        GPIO.setup([left_servo_pin, right_servo_pin], GPIO.OUT)
        self.left_servo_ctrl = GPIO.PWM(left_servo_pin, 50)
        self.right_servo_ctrl = GPIO.PWM(right_servo_pin, 50)

    def servo_angle_to_duty_cycle(self, angle):
        '''
            angle: servo angle, positive number between 0 and 180.
            returns a % between DUTY_CYCLE_MIN and DUTY_CYCLE_MAX
        '''
        return (angle / 18 + DUTY_CYCLE_MIN)

    def pwm_settings_to_pwm_freq(self, clk_div, pwm_range):
        '''
            returns the pwm frequency in Hz given the settings chosen
            the lowest possible pwm frequency is ~1.14 Hz (or tau ~= 0.88 s)
            the highest is the base frequency (19.2 MHz)
            https://raspberrypi.stackexchange.com/questions/4906/control-hardware-pwm-frequency
            For servo control we want to aim for one pulse per 20 ms, or 50 Hz
        '''
        return (RPI_PWM_BASE_FREQ / clk_div / pwm_range)

    def neutral(self):
        '''
            Operate both the left and right sides at neutral.
            The robot won't move.
            This has to be called before calling movement-related routines.
        '''

        self.left_servo_ctrl.start(LEFT_DC)
        self.right_servo_ctrl.start(RIGHT_DC)
        return

    def move(self, distance):
        '''
            move forward/backward by distance centimeters (negative for backward)
        '''

        # Use experimentally obtained lookup table to map from
        #     real-world distance to angular servo position
        degrees = distance # temporary stand-in

        # self.left_servo.angle = degrees
        # self.right_servo.angle = degrees
        self.left_servo_ctrl.ChangeDutyCycle(LEFT_DC-1.0)
        self.right_servo_ctrl.ChangeDutyCycle(RIGHT_DC+1.0)
        sleep(3) # sleep for the right amount of time to reach distance cm
        self.left_servo_ctrl.ChangeDutyCycle(LEFT_DC)
        self.right_servo_ctrl.ChangeDutyCycle(RIGHT_DC)
        return

    def pivot_turn_left(self, degrees):
        ''' forwards right servo and reverses left servo to turn left '''
        self.left_servo_ctrl.ChangeDutyCycle(LEFT_DC+0.5)
        self.right_servo_ctrl.ChangeDutyCycle(RIGHT_DC+0.5)
        sleep(2)
        self.left_servo_ctrl.ChangeDutyCycle(LEFT_DC)
        self.right_servo_ctrl.ChangeDutyCycle(RIGHT_DC)
        return

    def pivot_turn_right(self, degrees):
        ''' forwards left servo and reverses right servo to turn right '''
        self.left_servo_ctrl.ChangeDutyCycle(LEFT_DC-0.5)
        self.right_servo_ctrl.ChangeDutyCycle(RIGHT_DC-0.5)
        sleep(2)
        self.left_servo_ctrl.ChangeDutyCycle(LEFT_DC)
        self.right_servo_ctrl.ChangeDutyCycle(RIGHT_DC)
        return

    def turn_head(self, degrees):
        ''' turns the end effector/head by a certain # of degrees '''
        # on hiatus
        # self.headrot_servo.angle = degrees # WIP
        return

    def tilt_head(self, degrees):
        '''
            tilts the end effector/head forward or backwards by a certain
            # of degrees.
            Positive degrees indicates forwards.
            Negative degrees indicates backwards.
        '''
        # on hiatus
        # self.headtilt_servo.angle = degrees
        return

    def read_encoder(self, encoder):
        '''
            Returns the rotational velocity of an optical encoder.
            Currently in hiatus due to poor h/w quality
        '''
        return

    def test_run(self):

        print("Testing neutral position")
        self.neutral()
        sleep(2)

        print("Testing moving forward")
        self.move(50)
        sleep(2)

        # stop the PWMs and clean up resources
        self.left_servo_ctrl.stop()
        self.right_servo_ctrl.stop()
        GPIO.cleanup()

        return
