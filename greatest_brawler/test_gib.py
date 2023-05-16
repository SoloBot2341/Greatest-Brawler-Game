# test_ghib.py
import pygame
import sys
from simpleGhib import SimpleGhibs

pygame.init()

# Basic setup
width, height = 700, 700
screen = pygame.display.set_mode((width, height))
background_color = (0, 0, 0)
game_on = True
fps = pygame.time.Clock()

# Create a Ghibs instance
ghib = SimpleGhibs(screen, 300, 200)


while game_on:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_on = False

    # Clear the screen
    screen.fill(background_color)

    # Update Ghib
    ghib.update(screen)

    # Update the display
    pygame.display.update()
    pygame.display.flip()
    fps.tick(60)

pygame.quit()
sys.exit()
