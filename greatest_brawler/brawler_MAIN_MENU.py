import pygame
import sys
#Main menu screen module import Ghibs

pygame.init()

class MainMenu(object):
    def __init__(self,screen,x,y,width,height):
        self.blank_state = (0,0,0)
        super().__init__()
        #basic set up and loading images
        self.selected_character = None
        self.screen = screen
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.Main_Menu_screen = pygame.image.load("brawl_main_menu_screen.png")
        self.character_pick_screen = pygame.image.load("brawler_character_picker_screen.png")

        #dictionary for character selection
        self.ghibs_sel_x = (0,200)
        self.ghibs_sel_y = (140,345)
        self.ghibs_selected = (self.ghibs_sel_x, self.ghibs_sel_y)

        self.jasper_sel_x = (360,600)
        self.jasper_sel_y = (140,345)
        self.jasper_selected = (self.jasper_sel_x,self.jasper_sel_y)

        self.character_select_ranges = {"ghibs":[self.ghibs_selected,False],
                                        "jasper":[self.jasper_selected,False]}




        #ranges for buttons here
        self.one_player_mode_x = (135,436)
        self.one_player_mode_y = (69,118)
        self.one_player_mode = (self.one_player_mode_x,self.one_player_mode_y)

        self.multiplayer_mode_x = (143,570)
        self.multiplayer_mode_y = (120,167)
        self.multiplayer_mode = (self.multiplayer_mode_x,self.multiplayer_mode_y)

        self.characters_mode_x = (145,505)
        self.characters_mode_y = (180,225)
        self.characters_info_mode = (self.characters_mode_x,self.characters_mode_y)

        self.music_mode_x = (145,305)
        self.music_mode_y = (227,280)
        self.music_options_mode = (self.music_mode_x,self.music_mode_y)

        #set modes
        self.menu_screen_on = True
        self.one_player_selected = False
        self.multiplayer_selected = False
        self.character_info_selected = False
        self.music_options_mode_selected = False


    #menu screen logic here    
    def menu_screen(self,events):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                #check if the player clicks on a option
                self.mouse_x, self.mouse_y = pygame.mouse.get_pos()
                if self.one_player_mode_x[0] <= self.mouse_x <= self.one_player_mode_x[1] and self.one_player_mode_y[0] <= self.mouse_y <= self.one_player_mode_y[1]:
                    self.one_player_selected = True
                    self.menu_screen_on = False

                elif self.multiplayer_mode_x[0] <= self.mouse_x <= self.multiplayer_mode_x[1] and self.multiplayer_mode_y[0] <= self.mouse_y <= self.multiplayer_mode_y[1]:
                    self.multiplayer_selected = True
                    self.menu_screen_on = False
                elif self.music_mode_x[0] <= self.mouse_x <= self.music_mode_x[1] and self.music_mode_y[0] <= self.mouse_y <= self.music_mode_y[1]:
                    self.music_options_mode_selected = True
                    self.menu_screen_on = False
                elif self.characters_mode_x[0] <= self.mouse_x <= self.characters_mode_x[1] and self.characters_mode_y[0] <= self.mouse_y <= self.characters_mode_y[1]:
                    self.character_info_selected = True
                    self.menu_screen_on = False

                
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    quit()        

        self.screen.blit(self.Main_Menu_screen,(self.x,self.y))


    def one_player_game(self,events):
        #handle basic events
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    quit() 
                elif event.key == pygame.K_LCTRL:
                    self.menu_screen_on = True
                    self.one_player_selected = False
                    
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.mouse_x, self.mouse_y = pygame.mouse.get_pos()
                #check if the player clicks on a character option
                if self.ghibs_sel_x[0] <= self.mouse_x <= self.ghibs_sel_x[1] and self.ghibs_sel_y[0] <= self.mouse_y <= self.ghibs_sel_y[1]:
                    self.one_player_selected = False
                    self.character_select_ranges["ghibs"][1] = True
                if self.jasper_sel_x[0] <= self.mouse_x <= self.jasper_sel_x[1] and self.jasper_sel_y[0] <= self.mouse_y <= self.jasper_sel_y[1]:
                    self.one_player_selected = False
                    self.character_select_ranges["jasper"][1] = True


                        
        #blit the scrren                                           
        self.screen.blit(self.character_pick_screen,(self.x,self.y))


    
    def multi_player_game(self,events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    quit() 
                if event.key == pygame.K_LCTRL:
                    self.menu_screen_on = True
                    self.multiplayer_selected = False

        self.screen.fill(self.blank_state)


    #this function is for the music option
    def music_screen(self,events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    quit()        
                if event.key == pygame.K_LCTRL:
                    self.menu_screen_on = True
                    self.music_options_mode_selected = False
        self.screen.fill(self.blank_state)
        pass

    #character information option
    def character_info_mode(self,events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    quit()    
                if event.key == pygame.K_LCTRL:
                    self.menu_screen_on = True   
                    self.character_info_selected = False 
        self.screen.fill(self.blank_state)
        pass
    
    #function that calls everything
    def update(self,screen):
        events = pygame.event.get()
        if self.menu_screen_on == True:
            self.menu_screen(events)

        elif self.one_player_selected == True:
             self.one_player_game(events)
        elif self.multiplayer_selected == True:
            self.multi_player_game(events)
        elif self.character_info_selected == True:
            self.character_info_mode(events)
        elif self.music_options_mode_selected == True:
            self.music_screen(events)
        
        
        for character, (char_ranges, chars) in self.character_select_ranges.items():
            if chars:
                self.selected_character = character
                print(self.selected_character)


        
        pygame.display.update()
        pygame.display.flip()

    
    
        

