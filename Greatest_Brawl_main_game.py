import pygame
from pygame import mixer
import sys
import os
from brawler_MAIN_MENU import MainMenu
from Greatest_brawler_ghibs import Ghibs
from brawler_choose_map import Map
from jasper_brawler import Jasper
from Greatest_brawler_Collisions import PVAi

pygame.init()

#game winner window
game_winner_img = pygame.image.load("pixil-frame-0 (21).png")
font = pygame.font.Font(None,55)
winner_font = font.render("EASY WINS!",True,(255,255,255))
loser_font = font.render("TRASH CAN!",True,(255,255,255))
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
if main_menu.is_music == True:
    pygame.mixer.music.play(-1)
else:
    pygame.mixer.music.fadeout(1000)

#map choice menu
current_map = Map(screen,0,0,width,height)

#load the other character if 1p and detect collisions
pvp = PVAi(screen,500,390,10)

#defining the characters
#paramters(x,y,hp,energy)
ghib = Ghibs(30,390,200,200)

jasper = Jasper(screen,30,390,200,200)


#defining game states
main_menu_state = True # main menu
choose_map_state = False # choose a map
combat_state = False #the action and fun starts
Game_winner_state = False # This state displays the winner
Two_Player_State = False # This state displays when the multiplayer option is selected
game_state = main_menu_state # start off with the main menu


#handling collisions here
def collisions_jasper(enemy):
    torch = False
    ai_torch = False
    if jasper.magic_ball.rect.colliderect(pvp.cur_char.rect) and pvp.cur_char.image == pvp.cur_char.blocking_img_L or pvp.cur_char.image == pvp.cur_char.blocking_img_R:
        if jasper.attack_animation:
            if pvp.cur_char.shield_hp > 0:
                pvp.cur_char.shield_hp -= jasper.magic_ball.damage
                if pvp.cur_char.shield_hp < 0:
                    pvp.cur_char.shield_hp = 0

    elif pvp.cur_char.rect.colliderect(jasper.magic_ball.rect):
        if jasper.attack_animation:
            pvp.cur_char.hp -= jasper.magic_ball.damage

    
    elif pvp.cur_char.rect.colliderect(jasper.flamethrower_inst.rect):
        if jasper.flamethrower_animate:
            torch = True
            pvp.cur_char.hp -= jasper.flamethrower_inst.damage
            if torch and pvp.cur_char.hp != 0:
                pvp.cur_char.hp -= .5
            if pvp.cur_char.hp == 0:
                torch = False

def collisions_ghibs(enemy):
    if ghib.is_blocking_L or ghib.is_blocking_R:
        if ghib.image == ghib.blocking_img_L or ghib.image == ghib.blocking_img_R:
            if enemy.rect.colliderect(ghib.rect):
                ghib.shield_hp -= 7
    
    if ghib.is_attacking_R or ghib.is_attacking_L:
        if ghib.rect.colliderect(enemy.rect):
            enemy.hp -= .3
            enemy.rect.y -= 10
        if ghib.is_impact_R or ghib.is_impact_L:
            if ghib.rect.colliderect(enemy.rect):
                enemy.rect.y -= 10
                enemy.hp -= .8


   

while GAME_ON:
    if game_state == main_menu_state and main_menu_state == True:
        screen.fill(blank_state)
        main_menu.update(screen)
        for character, values in main_menu.character_select_ranges.items():
            selected, boolean = values
            if boolean:
                choose_map_state = True
                main_menu_state = False
                if choose_map_state:
                    game_state = choose_map_state


    elif game_state == choose_map_state:
        screen.fill(blank_state)
        current_map.update(screen)
        if current_map.selected_map:
            choose_map_state = False
            combat_state = True
            if combat_state:
                game_state = combat_state


    elif game_state == combat_state and combat_state == True:
        winner = None
        loser = None
        screen.fill(blank_state)  # Add this line to clear the screen
        current_map.screen.blit(current_map.selected_map, (current_map.x, current_map.y))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
            elif event.type == pygame.KEYUP:
                jasper.key_up(event)


        # Get the state of all keyboard buttons and update the character's position
        keys = pygame.key.get_pressed()
        ghib.key_down(keys)

       

        pvp.update(ghib if main_menu.selected_character == "ghibs" else jasper,screen)
        collisions_jasper(pvp.cur_char)
        collisions_ghibs(pvp.cur_char)

        #get the winners and loser for if jasper was selected
        if main_menu.selected_character == "jasper":
            jasper.update(width,height)
            if pvp.cur_char.hp <= 0:
                winner = jasper
                loser = pvp.cur_char
                loser.image = pvp.cur_char.base_img
            if jasper.hp <= 0:
                winner = pvp.cur_char
                loser = jasper
                winner.image = pvp.cur_char.base_img
        #gets winners and losers for if ghibs was selected
        elif main_menu.selected_character == "ghibs":
            ghib.update(screen)
            if pvp.cur_char.hp <= 0:
                winner = ghib
                loser = pvp.cur_char
                loser.image = pvp.cur_char.base_img
            if ghib.hp <= 0:
                winner = pvp.cur_char
                loser = ghib
                winner.image = pvp.cur_char.base_img


        
        #switch states once we have a winner and loser
        if winner and loser:
            Game_winner_state = True
            if Game_winner_state:
                combat_state = False
                game_state = Game_winner_state

    
    
    elif game_state == Game_winner_state and Game_winner_state == True:
        screen.fill(blank_state)
        screen.blit(game_winner_img,(0,0))
        screen.blit(winner.image,(400,390))
        screen.blit(winner_font,(350,350))
        screen.blit(loser.image,(100,390))
        screen.blit(loser_font,(0,350))

        menu_button_x = (0,450)
        menu_button_y = (500,630)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                    quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                #check if the player clicks on a option
                mouse_x, mouse_y = pygame.mouse.get_pos()

                if menu_button_x[0] <= mouse_x <= menu_button_x[1] and menu_button_y[0] <= mouse_y <=menu_button_y[1]:
                    main_menu_state = True
                    if main_menu_state == True:
                        pygame.quit()
                        sys.exit()


    pygame.display.flip()
    pygame.display.update()
    fps.tick(60)

pygame.quit()
sys.exit()

