from machine import Pin

def define_pins(pin_number):
    pin = Pin(pin_number, Pin.OUT)
    return pin, pin_number