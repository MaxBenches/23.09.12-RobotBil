import usocket as socket
import network
import pygame
from machine import Pin


static_ip = "192.168.1.102"  # Set IP addressen til PICO nr. 1
subnet_mask = "255.255.255.0"  # subnet mask
gateway = "192.168.1.1"  # gateway/router IP address
dns_server = "8.8.8.8"


wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect("wifi_ssid", "wifi_password")
#wlan.config((static_ip, subnet_mask, gateway, dns_server))

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
dest_ip = "PICO_2_IP_ADDRESS"
dest_port = 12345

print("Target IP:", dest_ip)
print("Target Port:" dest_port)

def main():
    sock.bind