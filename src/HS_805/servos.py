# High-level servo control & optical encoder read routines.

from gpiozero import Servo
from time import sleep

class ServoControl:
    '''
        Servo control interface.
        Provides access to high-level servo control methods
    '''

    # PWM-capable GPIOs on the RPi 4
    PWM0_PIN = 18  # GPIO-mode pin #
    PWM0_WPI = 1   # equivalent wiringPi pin
    SOFTPWM_PIN = 3 # GPIO-mode s/w pwm pin 12

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
    LEFT_SERVO_PIN  = 23
    RIGHT_SERVO_PIN = 24

    def __init__(self):
        left_servo  = Servo(LEFT_SERVO_PIN)
        right_servo = Servo(RIGHT_SERVO_PIN)

    def test_run(self):
        print("Testing servo min()")
        left_servo.min()
        right_servo.min()
        sleep(2)
        print("Testing servo mid()")
        left_servo.mid()
        right_servo.mid()
        sleep(2)
        print("Testing servo max()")
        left_servo.max()
        right_servo.max()
        sleep(2)

        return

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

    def pivot_turn_left(self, degrees):
        ''' forwards right servo and reverses left servo to turn left '''
        return

    def pivot_turn_right(self, degrees):
        ''' forwards left servo and reverses right servo to turn right '''
        return

    def read_encoder(self, encoder):
        '''
            Returns the rotational velocity of an optical encoder.
            Currently in hiatus due to poor h/w
        '''
        return
