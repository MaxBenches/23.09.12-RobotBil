import time
import machine

# Pico onboard LED assigned to led00
led00 = machine.Pin("LED", machine.Pin.OUT)

"""Blink onboard LED"""
# For MicroPython. Needs 'machine' and 'time' modules,
# as well as the led00 variable
# The functions blinks the onboard LED a specified
# (x) amount of times, when Pico boots.
def pico_blink(x):
    for i in range(x):
        led00.on()
        time.sleep(.2)
        led00.off()
        time.sleep(.2)