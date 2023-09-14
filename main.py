import machine
import time
import network
import socket

def main():
    motor_stop_2()
    sock.bind((UDP_IP, UDP_PORT))
    blink_pico(3)

    while True:
        message = msg_receive(1024, "utf-8")
        if message == "y1":
            motor_forward()
            print("Forward")   # Test
        elif message == "y-1":
            motor_backward()
            print("Backward")  # Test
        elif message == "A":
            motor_stop_2()
            print("Motor Stop")


""" PIN ASSIGNMENTS """
# Pico onboard LED assigned to led00
led00 = machine.Pin("LED", machine.Pin.OUT)

# H-Bro Inputs
IN1 = machine.Pin(0, machine.Pin.OUT)
IN2 = machine.Pin(1, machine.Pin.OUT)
IN3 = machine.Pin(2, machine.Pin.OUT)
IN4 = machine.Pin(3, machine.Pin.OUT)

# PWM Pin
pwmA = machine.PWM(machine.Pin(4))
pwmB = machine.PWM(machine.Pin(5))

""" MAGIC NUMBERS """
# Dutycycle / Speed of the motor
dutycycle_up = .5
dutycycle_down = .5
dutycycle_stop = 0





# PWM frequency
pwmA.freq(2000)
pwmB.freq(2000)


""" FUNCTIONS """

"""Motor functions"""
# This functions turns on the corresponding pins to drive upwards
def motor_forward():
    IN1.on()
    IN2.off()
    IN3.on()
    IN4.off()
    pwmA.duty_u16(int(65536 * dutycycle_up))
    pwmB.duty_u16(int(65536 * dutycycle_up))

# This functions turns on the corresponding pins to drive downwards
def motor_backward():
    IN1.off()
    IN2.on()
    IN3.off()
    IN4.on()
    pwmA.duty_u16(int(65536 * dutycycle_down))
    pwmB.duty_u16(int(65536 * dutycycle_down))

# This functions turns off the pins to stop the motor
# while maintaining a load on the motor
def motor_stop_2():
    IN1.off()
    IN2.off()
    IN3.off()
    IN4.off()
    pwmA.duty_u16(int(65536 * dutycycle_stop))
    pwmB.duty_u16(int(65536 * dutycycle_stop))


"""Blink onboard LED"""
# For MicroPython. Needs 'machine' and 'time' modules,
# as well as the led00 variable
# The functions blinks the onboard LED a specified
# (x) amount of times, when Pico boots.
def blink_pico(x):
    for i in range(x):
        led00.on()
        time.sleep(.2)
        led00.off()
        time.sleep(.2)

# This function receives a UDP message, decodes it
# and then prints it to the console
# Buffersize and which decoding format
# needs to be specified as arguments
def msg_receive(buffer_size, utf_x):
    message = sock.recv(buffer_size)
    message_decoded = message.decode(utf_x)
    return message_decoded
    #print(message_decoded) # Used for test


""" UDP SETUP    """
UDP_IP = "0.0.0.0"
UDP_PORT = 5005
print("UDP target IP: %s" % UDP_IP)
print("UDP target port: %s" % UDP_PORT)
sock = socket.socket(socket.AF_INET,  # Internet
                     socket.SOCK_DGRAM)  # UDP
ssid = "ITEK 2nd"
password = "2nd_Semester_F23v"
station = network.WLAN(network.STA_IF)
station.active(True)
station.connect(ssid, password)
while station.isconnected() == False:
    pass
print(station.ifconfig())

main()