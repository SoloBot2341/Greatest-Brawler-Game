import pygame 
import os

jasper_basic_atk_folder = "jasper_basic_atk"

class magic_ball(pygame.sprite.Sprite):
    def __init__(self,x,y,damage):
        magic_ball_img = pygame.image.load("jasper's magic ball.png")

class Jasper(pygame.sprite.Sprite):
    def __init__(self,x,y,hp,energy):
        self.font = pygame.font.Font(None, 25)
        self.health_text = self.font.render("Health", True, (0, 0, 0))
        self.energy_text = self.font.render("Energy", True, (0, 0, 0))
        #hp bar colors
        self.red = (255,0,0)
        self.green = (0,255,0)
        #energy bar colors
        self.white = (255,255,255)
        self.blue = (29,17,220)
        super().__init__()
        self.jasper = pygame.image.load("jasper the ghost brawler.png")

        self.magic_attack_R_list = []
        self.magic_attack_L_list = []
        attacking_imgs = os.listdir(jasper_basic_atk_folder)
        for images in attacking_imgs:
            image_pathway = os.path.join(jasper_basic_atk_folder,images)
            booted_img = pygame.image.load(image_pathway)

            self.magic_attack_R_list.append(booted_img)

            flipped_atk_images = pygame.transform.flip(booted_img,True,False)
            self.magic_attack_L_list.append(flipped_atk_images)
        
        self.block_R_img = pygame.image.load("jasper_block_img.png")
        self.block_L_img = pygame.transform.flip(self.block_R_img,True,False)

        #basic variables
        self.img = self.jasper
        self.rect = self.img.get_rect()
        self.rect.x = x
        self.rect.y= y
        self.frame_sped = 0
        self.walk_sped = 5
        self.jump_grav = 1
        self.jump_height = 20
        self.velocity = self.jump_height
        self.energy = energy
        self.max_energy = 200
        self.energy_gain = .07
        self.shield_hp = 50
        self.hp = hp

        #boolean variables
        self.is_facing_R = True
        self.is_facing_L = False
        self.is_walking_R = False
        self.is_walking_L = False
        self.is_jumping_R = False
        self.is_jumping_L = False
        self.is_attacking_R = False
        self.is_attacking_L = False
        self.is_blocking_R = False
        self.is_blocking_L = False
    
    def energy_management(self):
        if self.energy < self.max_energy:
            self.energy += self.energy_gain

    def walking_right(self):
        self.rect.x += self.walk_sped
        pass
    def walking_left(self):
        self.rect.x -= self.walk_sped
        pass
    def attacking_right(self):
        if self.is_facing_R and self.is_attacking_R and not self.is_facing_L and not self.is_attacking_L and self.energy >= 0:
            self.energy -= 2
            self.frame_sped += 3
            if self.frame_sped >= len(self.magic_attack_R_list):
                self.frame_sped = 0
                self.is_impact_attack_finished = True
            self.image = self.magic_attack_R_list[int(self.frame_sped)]
            
        if self.energy < 10:
            self.image = self.magic_attack_R_list[0]
       


        pass
    def attacking_left(self):
        if not self.is_facing_R and not self.is_attacking_R and self.is_facing_L and self.is_attacking_L and self.energy >= 0:
            self.energy -= 2
            self.frame_sped += 3
            if self.frame_sped >= len(self.magic_attack_R_list):
                self.frame_sped = 0
                self.is_impact_attack_finished = True
            self.image = self.magic_attack_R_list[int(self.frame_sped)]
            
        if self.energy < 10:
            self.image = self.magic_attack_R_list[0]

        pass
    def jumping_right(self):
        pass
    def jumping_left(self):
        pass
    def blocking_right(self):
        if self.is_facing_R and self.is_blocking_R and not self.is_blocking_L and not self.is_facing_L and self.energy > 10 and self.shield_hp >0:
            self.energy -= .6
            self.image = self.block_R_img

        if self.energy < 10:
            self.image = self.magic_attack_R_list[0]
        
        if self.shield_hp <= 0:
            self.image = self.magic_attack_R_list[0]
            self.shield_hp += .5


        pass
    def blocking_left(self):
        if not self.is_facing_R and not self.is_blocking_R and self.is_blocking_L and self.is_facing_L and self.energy > 10 and self.shield_hp >0:
            self.energy -= .6
            self.image = self.block_L_img

        if self.energy < 10:
            self.image = self.magic_attack_L_list[0]
        
        if self.shield_hp <= 0:
            self.image = self.magic_attack_L_list[0]
            self.shield_hp += .5
        pass



    def key_down(self,keys):

        #walking right
        if keys[pygame.K_d]:
            self.rect.x += self.walk_sped
            self.is_walking_R = True
            self.is_facing_R = True
            self.is_facing_L= False
            self.is_walking_L = False
            self.walking_right()
        #walking left
        elif keys[pygame.K_a]:
            self.rect.x -= self.walk_sped
            self.is_facing_L = True
            self.is_walking_L = True
            self.is_walking_R = False
            self.is_facing_R = False
            self.walking_left()

        #blocking right
        elif keys[pygame.K_q]:
            if self.is_facing_R and not self.is_facing_L:
                self.is_blocking_R = True
                self.is_blocking_L = False
                self.blocking_right()
            #blocking left
            else:
                self.is_facing_L = True
                self.is_blocking_L = True
                self.is_blocking_R = False
                self.blocking_left()
        
        #attacking right
        elif keys[pygame.K_1]:
            if self.is_facing_R and not self.is_facing_L:
                self.is_attacking_R = True
                self.is_attacking_L = False
                self.attacking_right()
            #attacking left
            elif self.is_facing_L and not self.is_facing_R:
                self.is_attacking_L = True
                self.is_attacking_R = False
                self.attacking_left()

        # impact attacking right



        elif keys[pygame.K_SPACE] or keys[pygame.K_w]:
            if self.is_facing_R and not self.is_facing_L:
                self.is_jumping_R = True
                self.is_jumping_L = False
                self.jumping_right()

            elif self.is_facing_L and not self.is_facing_R:
                self.is_jumping_R = False
                self.is_jumping_L = True
                self.jumping_left()
    
    def update(self,screen):
        self.energy_management()
        if self.is_facing_L:
            screen.blit(self.jasper,(self.rect.x - 50,self.rect.y))
        else:
            screen.blit(self.jasper,self.rect)


            # Draw health bar
        pygame.draw.rect(screen, self.red, (0, 30, 200, 25))
        pygame.draw.rect(screen, self.green, (0, 30, self.hp, 25))
        screen.blit(self.health_text, (0, 30))

        # Draw energy bar
        pygame.draw.rect(screen, self.white, (0, 70, 200, 15))
        pygame.draw.rect(screen, self.blue, (0, 70, self.energy, 15))
        screen.blit(self.energy_text, (0, 70))



        
        


