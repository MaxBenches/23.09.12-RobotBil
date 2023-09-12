import network
import socket

"""UDP Setup"""
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


def udp_receive(buffersize):
    sock.recv(buffersize)

def connect(UDP_IP, UDP_PORT):
    sock.bind((UDP_IP, UDP_PORT))