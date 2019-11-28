# High-level servo control & optical encoder read routines.

from gpiozero import Servo
from gpiozero import AngularServo
from time import sleep

class ServoControl:
    '''
        Servo control interface.
        Provides access to high-level servo control methods.
    '''

    # PWM-capable GPIOs on the RPi 4
    PWM0_PIN = 18  # GPIO-mode pin #
    PWM0_WPI = 1   # its equivalent wiringPi pin

    # Servo duty cycle min and max (in %). Vary by manufacturer.
    # Experimentally we know the duty cycle that gives a still servo is ~6.5%
    DUTY_CYCLE_MIN = 2  # defaults
    DUTY_CYCLE_MAX = 12
    DUTY_CYCLE_NEUT = 6.5

    # RPi PWM clock base frequency
    RPI_PWM_BASE_FREQ = 19.2e6

    LEFT_ENCODER    = 0
    RIGHT_ENCODER   = 1
    LEFT_SERVO      = 0
    RIGHT_SERVO     = 1

    def __init__(self, left_servo_pin=23,
                       right_servo_pin=24,
                       headtilt_servo_pin=27,
                       headrot_servo_pin=22):

        # NB: Default pin settings are GPIO-mode.
        #       physically they're (resp.) 16, 18, 13, 15
        self.left_servo  = AngularServo(left_servo_pin, min_angle=-90, max_angle=90)
        self.right_servo = AngularServo(right_servo_pin, min_angle=-90, max_angle=90)
        self.headtilt_servo = AngularServo(headtilt_servo_pin, min_angle=-90, max_angle=90)
        self.headrot_servo = AngularServo(headrot_servo_pin, min_angle=-90, max_angle=90)

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

    def move(self, distance):
        ''' move forward/backward by distance centimeters (negative for backward)'''

        # Use experimentally obtained lookup table to map from
        #     real-world distance to angular servo position
        degrees = distance # temporary stand-in

        self.left_servo.angle = degrees
        self.right_servo.angle = degrees
        sleep(2) # sleep for the right amount of time to reach distance cm
        self.left_servo.angle = 0 # reset to zero
        self.right_servo.angle = 0
        return

    def pivot_turn_left(self, degrees):
        ''' forwards right servo and reverses left servo to turn left '''
        self.left_servo.angle = 35
        self.right_servo.angle = -35
        return

    def pivot_turn_right(self, degrees):
        ''' forwards left servo and reverses right servo to turn right '''
        self.left_servo.angle = -35
        self.right_servo.angle = 35
        return

    def turn_head(self, degrees):
        ''' turns the end effector/head by a certain # of degrees '''
        self.headrot_servo.angle = degrees # WIP
        return

    def tilt_head(self, degrees):
        '''
            tilts the end effector/head forward or backwards by a certain
            # of degrees.
            Positive degrees indicates forwards.
            Negative degrees indicates backwards.
        '''
        self.headtilt_servo.angle = degrees
        return

    def read_encoder(self, encoder):
        '''
            Returns the rotational velocity of an optical encoder.
            Currently in hiatus due to poor h/w
        '''
        return

    def test_run(self):
        print("Testing servo min()")
        self.left_servo.min()
        self.right_servo.min()
        sleep(2)
        print("Testing servo mid()")
        self.left_servo.mid()
        self.right_servo.mid()
        sleep(2)
        print("Testing servo max()")
        self.left_servo.max()
        self.right_servo.max()
        sleep(2)
        print("Testing tilt_head(35 degrees)")
        self.turn_head(35)
        sleep(2)
        print("Testing tilt_head(-35 degrees)")
        self.turn_head(-35)
        sleep(2)
        print("Testing moving forward")
        self.move(35)
        sleep(2)

        return
