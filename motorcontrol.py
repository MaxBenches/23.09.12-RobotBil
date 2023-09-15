import pins
import PWM

IN1 = pins.define_pins(0)
IN2 = pins.define_pins(1)
IN3 = pins.define_pins(2)
IN4 = pins.define_pins(3)
# IN1 on = fremad
# IN2 on = bagud
# IN3 on = fremad
# IN4 on = bagud

pwmM1 = PWM.define_pwm_pin(4, 2000)
pvmM2 = PWM.define_pwm_pin(5, 2000)

def M1(retning):
    # Fremad
    if retning >= 0:
        IN1.on()
        IN2.off()
        pwmM1.duty_u16(int(65536 * retning))

    # # Bagud
    elif retning <= 0:
        IN1.off()
        IN2.on()
        pwmM1.duty_u16(int(65536 * retning))

def M2(retning):
    # Fremad
    if retning >= 0:
        IN3.on()
        IN4.off()
        pwmM2.duty_u16(int(65536 * retning))

    # Bagud
    elif retning <= 0:
        IN3.off()
        IN4.on()
        pwmM2.duty_u16(int(65536 * retning))

def Mstop():
    IN1.off()
    IN2.off()
    IN3.off()
    IN4.off()
