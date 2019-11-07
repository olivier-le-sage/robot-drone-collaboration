/*
    High-level servo control & optical encoder reading routines.
    NB: Access to PWM hardware may require root access.
        This program may have to run as sudo for it to work.
*/

#ifndef _SERVOS_H_
#define _SERVOS_H_
#endif

#include <wiringPi.h>

/* PWM-capable GPIOs on the RPi 4 */
#define PWM0_PIN 18  // pin on physical board
#define PWM0_WPI 1   // equivalent wiringPi pin

/* Servo duty cycle min and max (in %). Vary by manufacturer. */
/* Experimentally we know the duty cycle that gives a still servo is ~6.5% */
#define DUTY_CYCLE_MIN 2  // defaults
#define DUTY_CYCLE_MAX 12

/* RPi PWM clock base frequency */
#define RPI_PWM_BASE_FREQ 19.2e6

#define LEFT_ENCODER  0
#define RIGHT_ENCODER 1
#define LEFT_SERVO    0
#define RIGHT_SERVO   1

/* Prototypes */
double servo_angle_to_duty_cycle(double angle);
double pwm_settings_to_pwm_freq(int clk_div, int pwm_range);
void pivot_turn_left(int degrees);
void pivot_turn_right(int degrees);
double read_encoder(int encoder); // returns rotational velocity
