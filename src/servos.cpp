/*
    High-level servo control & optical encoder reading routines.
    NB: Access to PWM hardware may require root access.
        This program may have to run as sudo for it to work.
*/

#include <stdio.h>
#include "servos.h"

/* angle: servo angle, positive number between 0 and 180. */
/* returns a % between DUTY_CYCLE_MIN and DUTY_CYCLE_MAX */
double servo_angle_to_duty_cycle(double angle) {
    return (angle / 18 + DUTY_CYCLE_MIN);
}

/*
    returns the pwm frequency in Hz given the settings chosen
    the lowest possible pwm frequency is ~1.14 Hz (or tau ~= 0.88 s)
    the highest is the base frequency (19.2 MHz)
    https://raspberrypi.stackexchange.com/questions/4906/control-hardware-pwm-frequency
*/
double pwm_settings_to_pwm_freq(int clk_div, int pwm_range) {
    return (RPI_PWM_BASE_FREQ / clk_div / pwm_range);
}


int main (void) {
    printf("===== Raspberry Pi PWM test program =====\n")

    wiringPiSetupGpio();
    pinMode(PWM0_PIN, PWM_OUTPUT);
    pwmWrite(PWM0_PIN, dir);
    pwmSetMode(PWM_MODE_MS); // choose between mark:space and balanced type PWM
    pwmSetRange(2000);
    pwmSetClock(192);
    pwmWrite(18,150);
    return 0;
}
