import pygame
import socket

"""UDP Setup"""
UDP_IP = "0.0.0.0"
UDP_PORT = 5005
print("UDP target IP: %s" % UDP_IP)
print("UDP target port: %s" % UDP_PORT)
sock = socket.socket(socket.AF_INET,  # Internet
                     socket.SOCK_DGRAM)  # UDP

# Allow controller input using pygame
pygame.joystick.init()

# Assign joystick count to variable
# The list iterates over the indices of the recognised controllers
controllers = [pygame.joystick.Joystick(x) for x in range(pygame.joystick.get_count())]
# Print the list of recognised controllers
print(controllers)

# Initialise pygame
pygame.init()

while True:
    # Controller button input handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            break
        if event.type == pygame.JOYAXISMOTION:
            # Controller Analog Stick Input Handling
            x_axis = round(pygame.joystick.Joystick(0).get_axis(0))
            y_axis = round(pygame.joystick.Joystick(0).get_axis(1)) * -1
            if x_axis == 1:
                sock.sendto(b"x1", ("10.120.0.96", 5005))
                print("x1")
            elif x_axis == -1:
                sock.sendto(b"x-1", ("10.120.0.96", 5005))
                print("x-1")
            elif y_axis == 1:
                sock.sendto(b"y1", ("10.120.0.96", 5005))
                print("y1")
            elif y_axis == -1:
                sock.sendto(b"y-1", ("10.120.0.96", 5005))
                print("y-1")


# Use later for button handling
"""        
# If a button is pressed down, do something
if event.type == pygame.JOYBUTTONDOWN:
    # Prints the button ID for pressed down button
    #print(event)
    if pygame.joystick.Joystick(0).get_button(0):
        player.change_color("blue")
"""