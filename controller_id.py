import pygame

# This code identifies controller ID's for buttons and axes

pygame.joystick.init()
controllers = [pygame.joystick.Joystick(x) for x in range(pygame.joystick.get_count())]
pygame.init()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pass
        if event.type == pygame.JOYBUTTONDOWN:
            print(event)
        if event.type == pygame.JOYAXISMOTION:
            print(event)