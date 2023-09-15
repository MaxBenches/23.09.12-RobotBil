from machine import Pin, PWM

def define_pwm_pin(pwm_pin, pwm_freq):
    pwm = PWM(Pin(pwm_pin))
    pwm.freq(pwm_freq)
    return pwm_pin, pwm_freq