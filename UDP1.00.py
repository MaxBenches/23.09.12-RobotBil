import network
import socket
import time
import machine

def main():
    blink(3)
    sock.bind((UDP_IP, UDP_PORT))

    while True:
        """Receive UDP"""
        #message = sock.recv(1024)
        #message_decoded = message.decode("utf-8")
        #print(message_decoded)
        #time.sleep(3)

        """Send UDP"""
        sock.sendto("Hello World", ("192.168.0.134", 5005))
        time.sleep(5)


"""Pin Assignment"""
# Pico onboard LED assigned to led00
led00 = machine.Pin("LED", machine.Pin.OUT)

"""Functions"""
def blink(x):
    for i in range(x):
        led00.on()
        time.sleep(.2)
        led00.off()
        time.sleep(.2)

def msg_send(message, IP_address, port):
    sock.sendto(message, (IP_address, port))

def msg_receive(buffer, utf_x):
    message = sock.recv(buffer)
    message_decoded = message.decode(utf_x)
    print(message_decoded)


"""UDP Setup"""
UDP_IP = "0.0.0.0"
UDP_PORT = 5005
print("UDP target IP: %s" % UDP_IP)
print("UDP target port: %s" % UDP_PORT)
sock = socket.socket(socket.AF_INET,  # Internet
                     socket.SOCK_DGRAM)  # UDP
ssid = "BenchNet" #"ITEK 2nd"
password = "happyjungle592" #"2nd_Semester_F23v"
station = network.WLAN(network.STA_IF)
station.active(True)
station.connect(ssid, password)
while station.isconnected() == False:
    pass
print(station.ifconfig())


main()