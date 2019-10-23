/*
    High-level servo control & optical encoder reading routines.
    NB: Access to PWM hardware may require root access.
        This program may have to run as sudo for it to work.
*/

#ifndef _SERVOS_H_
#define _SERVOS_H_

#include <wiringPi.h>

/* PWM-capable GPIOs on the RPi 4 */
#define PWM0_PIN 18  // pin on physical board
#define PWM0_WPI 1   // equivalent wiringPi pin

/* Servo duty cycle min and max (in %). Vary by manufacturer. */
#define DUTY_CYCLE_MIN 2.5  // defaults
#define DUTY_CYCLE_MAX 12.5

/* RPi PWM clock base frequency */
#define RPI_PWM_BASE_FREQ 19.2e6

/* Prototypes */
double servo_angle_to_duty_cycle(double angle);
double pwm_settings_to_pwm_freq(int clk_div, int pwm_range);
void pivot_turn_left(int degrees);
void pivot_turn_right(int degrees);
int read_left_encoder(); // returns rotational velocity
int read_right_encoder();
