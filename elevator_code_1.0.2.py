import machine
import time
import socket
import network

"""UDP Setup"""
UDP_IP = "0.0.0.0"
UDP_PORT = 5005
print("UDP target IP: %s" % UDP_IP)
print("UDP target port: %s" % UDP_PORT)
sock = socket.socket(socket.AF_INET,  # Internet
                     socket.SOCK_DGRAM)  # UDP
ssid = "ITEK 1st"
password = "ITEK.drumBoy.F23v"
station = network.WLAN(network.STA_IF)
station.active(True)
station.connect(ssid, password)
while station.isconnected() == False:
    pass
print(station.ifconfig())

"""Pin Assignments"""
# Afstandssensor
gy53 = machine.Pin(0, machine.Pin.IN)

# Pico onboard LED assigned to led00
led00 = machine.Pin("LED", machine.Pin.OUT)

# H-Bro Inputs
IN1 = machine.Pin(1, machine.Pin.OUT)
IN2 = machine.Pin(2, machine.Pin.OUT)

# Assign buzzer to pin
buzzer = machine.PWM(machine.Pin(22))
# Set duty cycle to 0 to turn off buzzer
buzzer.duty_u16(0)

# Assign display pins

seg_A = machine.Pin(18, machine.Pin.OUT)
seg_B = machine.Pin(17, machine.Pin.OUT)
seg_C = machine.Pin(16, machine.Pin.OUT)
seg_D = machine.Pin(15, machine.Pin.OUT)
seg_E = machine.Pin(14, machine.Pin.OUT)
seg_F = machine.Pin(13, machine.Pin.OUT)
seg_G = machine.Pin(12, machine.Pin.OUT)

pins = [seg_A, seg_B, seg_C, seg_D, seg_E, seg_F, seg_G]

# This list of 10 numbers shows the states of the pins for the segments
# to display the appropriate number.
# Index the list to display the correct number.

# numbers = [zero, one, two, three, four, five, six, seven, eight, nine, clear display]
numbers = [[1, 1, 1, 1, 1, 1, 0],
           [0, 1, 1, 0, 0, 0, 0],
           [1, 1, 0, 1, 1, 0, 1],
           [1, 1, 1, 1, 0, 0, 1],
           [0, 1, 1, 0, 0, 1, 1],
           [1, 0, 1, 1, 0, 1, 1],
           [1, 0, 1, 1, 1, 1, 1],
           [1, 1, 1, 0, 0, 0, 0],
           [1, 1, 1, 1, 1, 1, 1],
           [1, 1, 1, 0, 0, 1, 1],
           [0, 0, 0, 0, 0, 0, 0]]

# Number to clear display
clear_display = 10

"""Magic Numbers"""
# Dutycycle / Speed of the motor
dutycycle_up = .7
dutycycle_down = .7
dutycycle_stop = 0

# PWM Pin
pwm = machine.PWM(machine.Pin(3))

# PWM frquency
pwm.freq(20000)

# Etage højder
etage_0 = 8
etage_1 = 15
etage_2 = 24

def main():
    motor_stop()
    display_number(10)
    blink(3)

    sock.bind((UDP_IP, UDP_PORT))
    while True:
        while True:
            # Measure height
            diff_us = time_measure()
            sensor_højde = convert_time_to_cm(diff_us)
            print(f"Sensor højde: {sensor_højde}cm.")

            # Recieve floor from UDP message
            message = sock.recv(1024)
            message_decoded = message.decode("utf-8")
            print(message_decoded)

            # Go to floor 2
            if message_decoded == "2":
                if sensor_højde < etage_2:
                    motor_up()
                    while sensor_højde < etage_2:
                        # Measure height
                        diff_us = time_measure()
                        sensor_højde_ny = convert_time_to_cm(diff_us)
                        print(f"Sensor højde ny: {sensor_højde_ny}")
                        if sensor_højde_ny >= etage_2:
                            motor_stop()
                            display_number(2)
                            play_melody()
                            break

            # Go to floor 1 - Up
            if message_decoded == "1":
                if sensor_højde < etage_1:
                    motor_up()
                    while sensor_højde < etage_1:
                        # Measure height
                        diff_us = time_measure()
                        sensor_højde_ny = convert_time_to_cm(diff_us)
                        print(f"Sensor højde ny: {sensor_højde_ny}")
                        if sensor_højde_ny >= etage_1:
                            motor_stop()
                            display_number(1)
                            play_melody()
                            break

            # Go to floor 1 - Down
            if message_decoded == "1":
                if sensor_højde > etage_1:
                    motor_down()
                    while sensor_højde > etage_1:
                        # Measure height
                        diff_us = time_measure()
                        sensor_højde_ny = convert_time_to_cm(diff_us)
                        print(f"Sensor højde ny: {sensor_højde_ny}")
                        if sensor_højde_ny <= etage_1 + 9:
                            motor_stop_2()
                            display_number(1)
                            play_melody()
                            break

            # Go to floor 0
            if message_decoded == "0":
                if sensor_højde > etage_0:
                    motor_down()
                    while sensor_højde > etage_0:
                        # Measure height
                        diff_us = time_measure()
                        sensor_højde_ny = convert_time_to_cm(diff_us)
                        print(f"Sensor højde ny: {sensor_højde_ny}")
                        if sensor_højde_ny <= etage_0:
                            motor_stop_2()
                            display_number(0)
                            play_melody()
                            break


"""Motor functions"""
# This functions turns on the corresponding pins to drive upwards
def motor_up():
    IN1.on()
    IN2.off()
    pwm.duty_u16(int(65536 * dutycycle_up))

# This functions turns on the corresponding pins to drive downwards
def motor_down():
    IN1.off()
    IN2.on()
    pwm.duty_u16(int(65536 * dutycycle_down))

# This functions turns off the pins to stop the motor
# while maintaining a load on the motor
def motor_stop_2():
    IN1.off()
    IN2.off()
    pwm.duty_u16(int(65536 * dutycycle_stop))

# This functions turns off the pins to stop the motor
def motor_stop():
    IN1.off()
    IN2.off()

"""Measure time and convert to distance"""
# This functions measures the time between 2 pulses
# and returns the difference between start and stop
def time_measure():
    while gy53.value() == True:
        pass
    while gy53.value() == False:
        pass
    time_start = time.ticks_us()
    while gy53.value() == True:
        pass
    time_end = time.ticks_us()
    diff_us = time_end - time_start
    return diff_us

# This function converts the time difference and converts it to
# the pulse width in both mm and cm, and returns those values
def convert_time_to_cm(time):
    pulse_width_cm = time / 100
    return pulse_width_cm

"""Blink onboard LED"""
# For MicroPython. Needs 'machine' and 'time' modules,
# as well as the led00 variable
# The functions blinks the onboard LED a specified
# (x) amount of times, when Pico boots.
def blink(x):
    for i in range(x):
        led00.on()
        time.sleep(.2)
        led00.off()
        time.sleep(.2)

"""Display Floor Number"""
#Display a number on a seven segment display

# This function takes in which number should be displayed,
# and then selects the correct pin/segment setup from
# the 'numbers' list to control the output pins
# To use the function in other projects the 'numbers' list,
# 'pin' variable, all the 'seg_X' variables,
# the 'clear display' variable and the 'machine' module are needed
def display_number(number_to_display):
    pin = 0
    for segment in range(7):
        pins[pin].value(numbers[number_to_display][segment])
        pin += 1
    return number_to_display

"""Play 'Solen er så rød, mor'"""
#Buzzer melody functions

def play_melody():
    # Set duty cycle to 0 to turn off buzzer
    buzzer.duty_u16(0)
    # Set a 50% duty cycle for the buzzer to produce a consistent tone
    buzzer.duty_u16(32767)
    # Play frequency / Pitch / Note
    buzzer.freq(784)    # G
    time.sleep_ms(375)  # Quarter Dotted
    # Put the 3 lines of code in a function to simplify
    buzzer.duty_u16(0)
    time.sleep(.05)
    buzzer.duty_u16(32767)
    buzzer.freq(784)    # G
    time.sleep_ms(125)  # Eight
    buzzer.duty_u16(0)
    time.sleep(.05)
    buzzer.duty_u16(32767)
    buzzer.freq(784)    # G
    time.sleep_ms(250)  # Quarter
    buzzer.duty_u16(0)
    time.sleep(.05)
    buzzer.duty_u16(32767)
    buzzer.freq(698)    # F
    time.sleep_ms(250)  # Quarter
    buzzer.duty_u16(0)
    time.sleep(.05)
    buzzer.duty_u16(32767)
    buzzer.freq(622)    # Eb
    time.sleep_ms(500)  # Half
    buzzer.duty_u16(0)
    time.sleep(.05)
    buzzer.duty_u16(32767)
    buzzer.freq(622)    # Eb
    time.sleep_ms(250)  # Quarter
    buzzer.duty_u16(0)
    time.sleep(.05)
    buzzer.duty_u16(32767)
    buzzer.freq(698)    # F
    time.sleep_ms(250)  # Quarter
    buzzer.duty_u16(0)
    time.sleep(.05)
    buzzer.duty_u16(32767)
    buzzer.freq(784)    # G
    time.sleep_ms(375)  # Quarter Dotted
    buzzer.duty_u16(0)
    time.sleep(.05)
    buzzer.duty_u16(32767)
    buzzer.freq(698)    # F
    time.sleep_ms(250)  # Eight
    buzzer.duty_u16(0)
    time.sleep(.05)
    buzzer.duty_u16(32767)
    buzzer.freq(784)    # G
    time.sleep_ms(250)  # Quarter
    buzzer.duty_u16(0)
    time.sleep(.05)
    buzzer.duty_u16(32767)
    buzzer.freq(831)    # Ab
    time.sleep_ms(250)  # Quarter
    buzzer.duty_u16(0)
    time.sleep(.05)
    buzzer.duty_u16(32767)
    buzzer.freq(932)    # Bb
    time.sleep_ms(1000)  # Whole
    buzzer.duty_u16(0)
    time.sleep(.05)
    buzzer.duty_u16(32767)
    buzzer.duty_u16(0)
main()