import socket
import pygame
import time

# Allow controller input using pygame
pygame.joystick.init()

# Assign joystick count to variable
# The list iterates over the indices of the recognised controllers
controllers = [pygame.joystick.Joystick(x) for x in range(pygame.joystick.get_count())]
# Print the list of recognised controllers
#print(controllers)

# Main Loop
def main():
    # Initialise pygame
    pygame.init()

    while True:
        # Print the start menu to Python console
        print_start_menu()

        while True:
            # Get controller input
            controller_input = get_controller_input()
            #print(controller_input)    # Prints infinitely, use only for test
            if controller_input == "Select":
                print("Exiting Program.")
                wait()
                quit()
            # Football loop
            if controller_input == "A":
                print("'Football Mode' selected.\n"
                      "To return to the menu press the 'Start' button.")
                while True:
                    controller_input = get_controller_input()
                    if controller_input == "Start":
                        print("Returning to menu")
                        wait()
                        break
                    elif controller_input == "B":
                        # Insert speaker honking
                        print("HONK HONK")
                    elif controller_input is not None:
                        msg_send(controller_input, "10.120.0.18", 5005)
                        print(controller_input)
                break

            # 'Follow the Wall' loop
            # Send a message to pico, so it knows what loop to go into
            if controller_input == "B":
                print("'Follow the Wall Mode' is under construction. Returning to menu.")
                wait()
                break

            # 'Move the Box' loop
            # Send a message to pico, so it knows what loop to go into
            if controller_input == "X":
                print("'Move the Box Mode' is under construction. Returning to menu.")
                wait()
                break


"""Socket binding"""
# Makes an internet (AF_INET) UDP (SOCK_DGRAM) socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

""" FUNCTIONS """

# This functions prints out a start menu and
# prompts the user for what they want to do
def print_start_menu():
    print("\nMenu:\n"
          "Football (Press 'A')\n"
          "Follow the Wall (Press 'B')\n"
          "Move the Box (Press 'X')\n"
          "Exit (Press 'Select')")

def input_validation(user_choice, num1, num2):
    while user_choice != num1 and user_choice != num2:
        print("\nNot a valid choice. Please choose a valid option from the menu.\n")
        print_start_menu()
        user_choice = int(input("What would you like to do?\n>> "))

def get_controller_input():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return None
        # Analog stick input handling
        if event.type == pygame.JOYAXISMOTION:
            x_axis = round(pygame.joystick.Joystick(0).get_axis(0))
            y_axis = round(pygame.joystick.Joystick(0).get_axis(1)) * -1
            left_trig = round(pygame.joystick.Joystick(0).get_axis(4))
            right_trig = round(pygame.joystick.Joystick(0).get_axis(5))
            if x_axis == 1:
                return "x1"
            elif x_axis == -1:
                return "x-1"
            elif y_axis == 1:
                return "y1"
            elif y_axis == -1:
                return "y-1"
            elif left_trig == 1:
                return "lt"
            elif right_trig == 1:
                return "rt"
        # Button input handling
        if event.type == pygame.JOYBUTTONDOWN:
            if pygame.joystick.Joystick(0).get_button(0):
                return "A"
            elif pygame.joystick.Joystick(0).get_button(1):
                return "B"
            elif pygame.joystick.Joystick(0).get_button(2):
                return "X"
            elif pygame.joystick.Joystick(0).get_button(3):
                return "Y"
            elif pygame.joystick.Joystick(0).get_button(6):
                return "Select"
            elif pygame.joystick.Joystick(0).get_button(7):
                return "Start"
    return None

# This function takes a message, as a string,
# encodes it with utf-8 and then sends it
# to an ip address via a specified port
def msg_send(message, ip_address, port):
    message_encoded = message.encode("utf-8")
    sock.sendto(message_encoded, (ip_address, port))

def wait():
    time.sleep(.3)

main()