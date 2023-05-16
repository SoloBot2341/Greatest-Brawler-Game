import pygame
import os

ghibs_attack_folder = "ghib_basic_attack"
ghibs_walkings_folder = "ghibs_walking_frames"
ghibs_impact_attack_folder = "ghib_super_attack"
ghibs_jumping_folder = "ghibs_jumping"


class Ghibs(pygame.sprite.Sprite):
    def __init__(self,x,y,hp):
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
        #load the images here
        self.walking_R_list = []
        self.walking_L_list = [] 

        walking_images = os.listdir(ghibs_walkings_folder)
        for images in walking_images:
            image_path = os.path.join(ghibs_walkings_folder, images)
            loaded_image = pygame.image.load(image_path)

            self.walking_R_list.append(loaded_image)
            # Flip the resized image
            flipped_image = pygame.transform.flip(loaded_image, True, False)
            self.walking_L_list.append(flipped_image)

        #blocking images
        self.blocking_img_R = pygame.image.load("resized shield frame.png")
        self.blocking_img_L = pygame.transform.flip(self.blocking_img_R, True, False)
 
        # Create a attacking list
        self.ghibs_attacking_R_list = []
        self.ghibs_attacking_L_list = []

        # Load images from the ghibs_attack_folder
        attack_images = os.listdir(ghibs_attack_folder)
        for image_file in attack_images:
            image_path = os.path.join(ghibs_attack_folder, image_file)
            loaded_image = pygame.image.load(image_path)


            self.ghibs_attacking_R_list.append(loaded_image)

            # Flip the resized image
            flipped_image = pygame.transform.flip(loaded_image, True, False)
            self.ghibs_attacking_L_list.append(flipped_image)
        
        self.ghib_impact_R_list = []
        self.ghib_impact_L_list = []
        for files in os.listdir(ghibs_impact_attack_folder):
            images = os.path.join(ghibs_impact_attack_folder,files)
            loaded_images = pygame.image.load(images)

            self.ghib_impact_R_list.append(loaded_images)
        
            flipped_images = pygame.transform.flip(loaded_images, True, False)
            self.ghib_impact_L_list.append(flipped_images)


        #basic game variables
        self.image = self.walking_R_list[0]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.y = y
        self.rect.x = x
        self.rect.y = y
        self.walk_sped = 5
        self.jump_grav =  4
        self.jump_height = 25 # are maximum velocity
        self.velocity = self.jump_height
        self.energy = 200
        self.max_energy = 200
        self.energy_gain = .07
        self.hp = hp
        self.frame_sped = 0.7
        self.shield_hp = 50


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
        self.is_impact_R = False
        self.is_impact_L = False
        self.is_in_air = False
        self.is_impact_attack_finished = False


    def energy_management(self):
        if self.energy < self.max_energy:
            self.energy += self.energy_gain

    
    def walk_right(self):
        if self.is_facing_R and not self.is_facing_L and self.is_walking_R and not self.is_walking_L:
            self.frame_sped += 0.3
            if self.frame_sped >= len(self.walking_R_list):
                self.frame_sped = 0
            self.image = self.walking_R_list[int(self.frame_sped)]
            pass


    def walk_left(self):
        if self.is_facing_L and not self.is_facing_R and self.is_walking_L and not self.is_walking_R:
            self.frame_sped += 0.3
            if self.frame_sped >= len(self.walking_L_list):
                self.frame_sped = 0
            self.image = self.walking_L_list[int(self.frame_sped)]
            pass
    
    def attacking_right(self):
        if self.is_facing_R and not self.is_facing_L and self.is_attacking_R and not self.is_attacking_L and self.energy >= 15:
            self.energy -= .3
            self.frame_sped += 2
            if self.frame_sped >= len(self.ghibs_attacking_R_list):
                self.frame_sped = 0
            self.image = self.ghibs_attacking_R_list[int(self.frame_sped)]
        if self.energy < 15:
            self.image = self.walking_R_list[0]
        pass
                    
    def attacking_left(self):
        if self.is_facing_L and not self.is_facing_R and self.is_attacking_L and not self.is_attacking_R and self.energy  >= 15:
            self.energy -= .3
            self.frame_sped += .3
            if self.frame_sped >= len(self.ghibs_attacking_L_list):
                self.frame_sped = 0
            self.image = self.ghibs_attacking_L_list[int(self.frame_sped)]
        if self.energy < 15:
            self.image = self.walking_L_list[0]
        pass

    def impact_attack_right(self):
        if self.is_facing_R and self.is_impact_R and not self.is_facing_L and not self.is_impact_L and self.energy >= 0:
            self.rect.x += 5
            self.energy -= 2
            self.frame_sped += 3
            if self.frame_sped >= len(self.ghib_impact_R_list):
                self.frame_sped = 0
                self.is_impact_attack_finished = True
            self.image = self.ghib_impact_R_list[int(self.frame_sped)]
            
        if self.energy < 10 or self.is_impact_attack_finished:
            self.image = self.walking_R_list[0]
            self.is_impact_attack_finished = False  # Reset the state for the next attack


    def impact_attack_left(self):
        if self.is_facing_L and self.is_impact_L and not self.is_facing_R and not self.is_impact_R and self.energy >= 0:
            self.rect.x -= 5
            self.energy -= 2
            self.frame_sped += 3
            if self.frame_sped >= len(self.ghib_impact_L_list):
                self.frame_sped = 0
                self.is_impact_attack_finished = True
            self.image = self.ghib_impact_L_list[int(self.frame_sped)]

        if self.energy < 10 or self.is_impact_attack_finished:
            self.image = self.walking_L_list[0]
            self.is_impact_attack_finished = False  # Reset the state for the next attack
        

    def jumping_right(self):
        if self.is_facing_R and not self.is_facing_L and self.is_jumping_R and not self.is_jumping_L:
            self.is_in_air = True
            print(f"the velocity is {self.velocity}")
            print(f"the rect y axis is {self.rect.y}")
            self.rect.y -= self.velocity
            self.velocity -= self.jump_grav
            if self.velocity <= -self.jump_height:
                self.is_jumping_R = False
                self.velocity = self.jump_height

                    
                
    def jumping_left(self):
       if self.is_facing_L and not self.is_facing_R and self.is_jumping_L and not self.is_jumping_R:
            self.is_in_air = True
            self.rect.y -= self.velocity
            self.velocity -= self.jump_grav
            if self.velocity <= -self.jump_height:
                self.is_jumping_L = False
                self.velocity = self.jump_height


    def gravity(self):
        if self.is_in_air:
            self.rect.y += self.jump_grav  # Change this to your desired gravity value
            if self.rect.y >= self.y:  # If the character is back on the ground
                self.rect.y = self.y
                self.is_in_air = False



    def blocking_right(self):
        if self.is_blocking_R and not self.is_blocking_L and not self.is_facing_L and self.is_facing_R and self.energy >= 10 and self.shield_hp > 0:
            self.energy -= .6
            self.image = self.blocking_img_R
        
        if self.shield_hp <= 0:
            self.image = self.walking_R_list[0]
            self.shield_hp += .5
        


        if self.energy < 10:
            self.image = self.walking_R_list[0]
            pass
    def blocking_left(self):
        if self.is_blocking_L and self.is_facing_L and not self.is_facing_R and not self.is_blocking_R and self.energy >= 10 and self.shield_hp > 0:
            self.energy -= .6
            self.image = self.blocking_img_L

        if self.energy < 10:
            self.image = self.walking_L_list[0]
        
        if self.shield_hp <= 0:
            self.image = self.walking_L_list[0]
            self.shield_hp += .5
            
    def key_down(self,keys):

        #walking right
        if keys[pygame.K_d]:
            self.rect.x += self.walk_sped
            self.is_walking_R = True
            self.is_facing_R = True
            self.is_facing_L= False
            self.is_walking_L = False
            self.walk_right()
        #walking left
        elif keys[pygame.K_a]:
            self.rect.x -= self.walk_sped
            self.is_facing_L = True
            self.is_walking_L = True
            self.is_walking_R = False
            self.is_facing_R = False
            self.walk_left()

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
        elif keys[pygame.K_2]:
            if self.is_facing_R and not self.is_facing_L:
                self.is_impact_R = True
                self.is_impact_L = False
                self.impact_attack_right()
            #impact attacking left
            elif self.is_facing_L and not self.is_facing_R:
                self.is_impact_R = False
                self.is_impact_L = True
                self.impact_attack_left()


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
            screen.blit(self.image,(self.rect.x - 50,self.rect.y))
        else:
            screen.blit(self.image,self.rect)
        

        #pygame.draw.rect(screen,self.green,self.rect)
        self.gravity()

        if self.is_jumping_R:
            self.jumping_right()
        elif self.is_jumping_L:
            self.jumping_left()
        

            # Draw health bar
        pygame.draw.rect(screen, self.red, (0, 30, 200, 25))
        pygame.draw.rect(screen, self.green, (0, 30, self.hp, 25))
        screen.blit(self.health_text, (0, 30))

        # Draw energy bar
        pygame.draw.rect(screen, self.white, (0, 70, 200, 15))
        pygame.draw.rect(screen, self.blue, (0, 70, self.energy, 15))
        screen.blit(self.energy_text, (0, 70))
