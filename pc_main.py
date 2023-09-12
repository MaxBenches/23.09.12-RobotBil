import socket
import pygame

# Allow controller input using pygame
pygame.joystick.init()

# Assign joystick count to variable
# The list iterates over the indices of the recognised controllers
controllers = [pygame.joystick.Joystick(x) for x in range(pygame.joystick.get_count())]
# Print the list of recognised controllers
#print(controllers)


def main():
    # Initialise pygame
    pygame.init()

    while True:
        controller_input = get_controller_input()
        if controller_input is not None:
            msg_send(controller_input, "192.168.0.132", 5005)
            print(controller_input)



"""Socket binding"""
# Makes an internet (AF_INET) UDP (SOCK_DGRAM) socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

""" FUNCTIONS """

# This function takes a message, as a string,
# encodes it with utf-8 and then sends it
# to an ip address via a specified port
def msg_send(message, ip_address, port):
    message_encoded = message.encode("utf-8")
    sock.sendto(message_encoded, (ip_address, port))

def get_controller_input():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return None
        # Analog stick input handling
        if event.type == pygame.JOYAXISMOTION:
            x_axis = round(pygame.joystick.Joystick(0).get_axis(0))
            y_axis = round(pygame.joystick.Joystick(0).get_axis(1)) * -1
            if x_axis == 1:
                return "x1"
            elif x_axis == -1:
                return "x-1"
            elif y_axis == 1:
                return "y1"
            elif y_axis == -1:
                return "y-1"
        # Button input handling
        if event.type == pygame.JOYBUTTONDOWN:
            if pygame.joystick.Joystick(0).get_button(0):
                return "Fodbold"
            elif pygame.joystick.Joystick(0).get_button(1):
                return "Vaeg"
            elif pygame.joystick.Joystick(0).get_button(2):
                return "Kasse"
    return None

main()