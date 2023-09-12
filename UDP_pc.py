"""UDP Setup"""
import socket


sock = socket.socket(socket.AF_INET,  # Internet
                     socket.SOCK_DGRAM)  # UDP


def UDP_send(message, user_IP_PORT):
    sock.sendto(bytes(message, "utf-8"), user_IP_PORT)
