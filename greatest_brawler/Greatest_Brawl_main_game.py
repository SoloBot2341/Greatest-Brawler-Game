import pygame
import sys
import os
from brawler_MAIN_MENU import MainMenu
from Greatest_brawler_ghibs import Ghibs
from brawler_choose_map import Map
from jasper_brawler import Jasper

pygame.init()

#basic setup
height = 700
width = 700
x_range = (0,701)
y_range = 455
screen = pygame.display.set_mode((width,height))
blank_state = (0,0,0)
GAME_ON = True
fps = pygame.time.Clock()

main_menu = MainMenu(screen,0,0,width,height)

#map choice menu
current_map = Map(screen,0,0,width,height)

#defining the characters
#paramters(x,y,hp,energy)
ghib = Ghibs(100,390,200)

jasper = Jasper(650,390,200,200)


#defining game states
main_menu_state = 0 # main menu
choose_map_state = 1 # choose a map
combat_state = 2 #the action and fun starts
game_state = main_menu_state # start off with the main menu

while GAME_ON:

    if game_state == main_menu_state:
        screen.fill(blank_state)
        main_menu.update(screen)
        for character, values in main_menu.character_select_ranges.items():
            selected, boolean = values
            if boolean:
                game_state = choose_map_state

    elif game_state == choose_map_state:
        screen.fill(blank_state)
        current_map.update(screen)
        if current_map.selected_map:
            game_state = combat_state

    elif game_state == combat_state:
        screen.fill(blank_state)  # Add this line to clear the screen
        current_map.screen.blit(current_map.selected_map, (current_map.x, current_map.y))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()

        # Get the state of all keyboard buttons and update the character's position
        keys = pygame.key.get_pressed()
        ghib.key_down(keys)
        jasper.key_down(keys)

        if main_menu.selected_character == "ghibs":
            ghib.update(screen)
        if main_menu.selected_character == "jasper":
            jasper.update(screen)


    pygame.display.flip()
    fps.tick(60)

pygame.quit()
sys.exit()

