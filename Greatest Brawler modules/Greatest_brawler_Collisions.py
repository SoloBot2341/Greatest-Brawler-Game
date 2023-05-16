import pygame
import random
from Greatest_Brawler_Ais import AIGhibs,AIJasper



class PVAi():
    def __init__(self,screen,x,y,damage):
        self.characters = {
            "ghib": AIGhibs(screen,x, y,400,200),
            "jasper": AIJasper(screen,x, y,400,200)
        }
        self.cur_char = None
        
        #basic variables
        self.x = x
        self.y = y
        self.damage = damage
        self.skill_affects = None
        self.screen = screen


    def spawn_random_character(self):
        # randomly select a character
        character_key = random.choice(list(self.characters.keys()))
        self.cur_char = self.characters[character_key]



    def update(self,enemy,screen):
        if not self.cur_char:
            self.spawn_random_character()
        elif self.cur_char:
            self.cur_char.update(enemy,screen)


