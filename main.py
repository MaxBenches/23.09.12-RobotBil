import machine
import time
import network
import socket

def main():
    sock.bind((UDP_IP, UDP_PORT))
    blink_pico(3)

    while True:
        msg_receive(1024, "utf-8")


""" PIN ASSIGNMENTS """
# Pico onboard LED assigned to led00
led00 = machine.Pin("LED", machine.Pin.OUT)


""" FUNCTIONS """

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
    print(message_decoded)


""" UDP SETUP    """
UDP_IP = "0.0.0.0"
UDP_PORT = 5005
print("UDP target IP: %s" % UDP_IP)
print("UDP target port: %s" % UDP_PORT)
sock = socket.socket(socket.AF_INET,  # Internet
                     socket.SOCK_DGRAM)  # UDP
ssid = "BenchNet"
password = "happyjungle592"
station = network.WLAN(network.STA_IF)
station.active(True)
station.connect(ssid, password)
while station.isconnected() == False:
    pass
print(station.ifconfig())

main()