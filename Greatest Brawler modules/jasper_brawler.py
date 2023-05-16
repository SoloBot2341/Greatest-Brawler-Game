import pygame 
import os
from pygame import mixer
from brawler_MAIN_MENU import MainMenu


jasper_basic_atk_folder = "greatest_brawler/jasper_basic_atk"
jasper_flame_thrower_folder = "jasper_flamethrower_folder"



class Magic_ball(pygame.sprite.Sprite):
    def __init__(self,x,y,damage):
        self.magic_ball_img = pygame.image.load("jasper_magic_ball.png")
        self.image = self.magic_ball_img
        self.rect = self.image.get_rect()
        self.y = y
        self.x = x
        self.rect.x = x
        self.rect.y = y
        self.damage = damage
        self.speed = 20

        #boolean
        self.moving = True


class flamethrower(pygame.sprite.Sprite):
    def __init__(self,x,y,damage):
        self.image = pygame.image.load("jasper_fire_ball_image.png")
        self.x = x
        self.y = y
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)  # set the position of the sprite
        self.speed = 20
        self.torching = False
        self.damage = damage
        #loop the images
        self.flamethrower_timer = 0
        self.flame_delay = 0  # set delay in milliseconds
        self.last_update = pygame.time.get_ticks()  # time of the last update
        self.flame_list = [] # list of flame ball images to make a flamethrower effect
        if len(self.flame_list) == 0:
            for _ in range(10):
                self.flame_list.append(self.image)



    def flamethrower_animation(self,screen,right,left):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.flame_delay:  # check if it's time to update
            self.last_update = now
            self.torching = True if self.flamethrower_timer < len(self.flame_list) else False

            if self.torching:
                image = self.flame_list[int(self.flamethrower_timer)]
               
                screen.blit(image, self.rect)
                if right:
                    self.rect.x += 10
                     # Add wave motion

                elif left:
                    self.rect.x -= 10

                    
                self.flamethrower_timer += 1
            else:
                self.flamethrower_timer = 0  # reset timer
                self.rect.y = self.y  # reset to original y-coordinate


class Jasper(pygame.sprite.Sprite):
    def __init__(self,screen,x,y,hp,energy):
        self.main_mens = MainMenu(None,None,None,None,None)
        self.screen = screen
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
        self.jasper = pygame.image.load("greatest_brawler/jasper the ghost brawler.png")
        self.jasper_L = pygame.transform.flip(self.jasper,True,False)

        self.magic_attack_R_list = []
        self.magic_attack_L_list = []
        attacking_imgs = os.listdir(jasper_basic_atk_folder)
        for images in attacking_imgs:
            image_pathway = os.path.join(jasper_basic_atk_folder,images)
            booted_img = pygame.image.load(image_pathway)

            self.magic_attack_R_list.append(booted_img)

            flipped_atk_images = pygame.transform.flip(booted_img,True,False)
            self.magic_attack_L_list.append(flipped_atk_images)


        #flamethrower skill
        self.flame_right_list = []
        self.flame_left_list = []
        flamethrower_imgs = os.listdir(jasper_flame_thrower_folder)
        for pic in flamethrower_imgs:
            pic_path_way = os.path.join(jasper_flame_thrower_folder,pic)
            ready_imgs = pygame.image.load(pic_path_way)

            self.flame_right_list.append(ready_imgs)
            flipped_flame_imgs = pygame.transform.flip(ready_imgs,True,False)
            self.flame_left_list.append(flipped_flame_imgs)
        
        self.block_R_img = pygame.image.load("greatest_brawler/jasper_block_img.png")
        self.block_L_img = pygame.transform.flip(self.block_R_img,True,False)


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
        self.is_in_air = False
        self.attack_animation = False
        self.shooting_magic_ball = False
        self.flamethrower_animate = False
        self.flamethrower_R = False
        self.flamethrower_L = False
        self.flame_frames = 0
        self.flamethrower_activate = False

        #basic variables
        if self.is_facing_R:
            self.image = self.jasper
        elif self.is_facing_L:
            self.image = self.magic_attack_L_list[0]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y= y
        # Calculate the center manually
        self.center = (self.rect.x + self.rect.width // 2, self.rect.y + self.rect.height // 2)

        self.y = y
        self.x = x
        self.frame_sped = 0
        self.walk_sped = 5 
        self.jump_height = 20
        self.jump_velocity = self.jump_height
        self.gravity = 1
        self.energy = energy
        self.max_energy = 200
        self.energy_gain = 1.5
        self.shield_hp = 50
        self.hp = hp
        self.offset_x = self.rect.x
        self.offset_y = self.rect.y
        self.ATTACK_COST = 10
        self.ANIMATION_SPEED = .8
        self.MAGIC_BALL_DAMAGE = 50


         #magic ball instance
        self.offset_x = 0
        self.offset_y = 25
        self.magic_ball = Magic_ball(self.center[0] - self.offset_x,self.center[1] - self.offset_y,1)
        self.flamethrower_inst = flamethrower(self.center[0] - self.offset_x,self.center[1] - self.offset_y - 105,.5)

        #state hasmap
        self.state_map = {"Attacking?": False,
                          "Chasing?":False,
                          "Defending?": False,
                          "Jumping?": False,
                          "Chasing?": False}
    
    
    def get_state(self):
        # Check the current action and update the state accordingly
        if self.shooting_magic_ball or self.flamethrower_activate:
            self.state_map["Attacking?"] = True
        if self.is_walking_R or self.is_walking_L:
            self.state_map["Chasing?"] = True
        if self.is_blocking_L or self.is_blocking_R:
            self.state_map["Defending?"] = True
        if self.is_in_air:
            self.state_map["Jumping?"] = True
        
        # Check if more than two actions are True and reset all to False if they are
        if sum(value for value in self.state_map.values()) > 1:
            self.state_map = {key: False for key in self.state_map}


    

#this function controls going or left and right
    def left_or_right(self):
        if self.is_facing_R or self.is_walking_R or self.is_jumping_R or self.is_attacking_R or self.is_blocking_R:
            self.is_facing_L = False
            self.is_walking_L = False
            self.is_jumping_L = False
            self.is_attacking_L = False
            self.is_blocking_L = False
        elif self.is_facing_L or self.is_walking_L or self.is_attacking_L or self.is_jumping_L or self.is_blocking_L:
            self.is_facing_R = False
            self.is_walking_R = False
            self.is_jumping_R = False
            self.is_attacking_R = False
            self.is_blocking_R = False
            
    #this function is called to balance energy consumption
    def energy_management(self):
        if self.energy < self.max_energy:
            self.energy += self.energy_gain

    #walking function 
    def walking(self):
        if self.is_walking_R:
            self.rect.x += 5
            self.image = self.magic_attack_R_list[0]
        elif self.is_walking_L:
            self.rect.x -= 5
            self.image = self.magic_attack_L_list[0]

    #jump function
    def jumping(self):
        if self.is_in_air:
            self.rect.y -= self.jump_velocity
            self.jump_velocity -= self.gravity
            if self.jump_velocity < -self.jump_height:
                self.is_in_air = False
                self.jump_velocity = self.jump_height
    
    #this function draws the basic attack of Jasper which uses a magic ball like image. This function is for both left and right.
    def drawing_magic_ball(self,width):
        if self.is_attacking_R:
            if round(self.frame_sped) == len(self.magic_attack_R_list)-1 and not self.shooting_magic_ball:
                # Update the position of the magic ball right when the attack is initiated
                self.magic_ball.rect.x = self.center[0] - self.offset_x
                self.magic_ball.rect.y = self.center[1] - self.offset_y
                self.shooting_magic_ball = True

            if self.shooting_magic_ball and self.is_attacking_R:
                self.screen.blit(self.magic_ball.image,self.magic_ball.rect)
                self.magic_ball.rect.x += self.magic_ball.speed

            if self.magic_ball.rect.x >= width + 100 :
                # Set shooting_magic_ball to False when the ball leaves the screen\
                self.shooting_magic_ball = False
        
        elif self.is_attacking_L:
            if round(self.frame_sped) == len(self.magic_attack_R_list)-1 and not self.shooting_magic_ball:
                self.magic_ball.rect.x = self.center[0] - self.offset_x - 200
                self.magic_ball.rect.y = self.center[1] - self.offset_y
                self.shooting_magic_ball = True

            if self.shooting_magic_ball and self.is_attacking_L:
                self.screen.blit(self.magic_ball.image,self.magic_ball.rect)
                self.magic_ball.rect.x -= self.magic_ball.speed

            
            if self.magic_ball.rect.x <=-100:
                self.shooting_magic_ball = False

    #this functiong is for attacking right with the basic attack
    def attacking_right(self):
        if self.is_attacking_R:
            if self.attack_animation and not self.shooting_magic_ball and self.is_facing_R:
                self.frame_sped += .9
                if self.frame_sped >= len(self.magic_attack_R_list):
                    self.frame_sped = 0
                    self.attack_animation = False
                self.image = self.magic_attack_R_list[int(self.frame_sped)]
    

    #this function is the basic attack for the left side
    def attacking_left(self):
        if self.is_attacking_L:
            if self.attack_animation and not self.shooting_magic_ball and self.is_facing_L:
                self.frame_sped += .9
                if self.frame_sped >= len(self.magic_attack_L_list):
                    self.frame_sped = 0
                    self.attack_animation = False
                self.image = self.magic_attack_L_list[int(self.frame_sped)]
    
    #this function draws the fire ball image
    def drawing_flamethrower(self,width):
        if self.flamethrower_R:
            if round(self.flame_frames) == len(self.flame_right_list)-1 and not self.flamethrower_activate:
                # Update the position of the magic ball right when the attack is initiated
                self.flamethrower_inst.rect.x = self.center[0] - self.offset_x
                self.flamethrower_inst.rect.y= self.center[1] - self.offset_y - 105
                self.flamethrower_activate = True

            if self.flamethrower_activate and self.flamethrower_R:
                self.flamethrower_inst.flamethrower_animation(self.screen,True,False)
                self.flamethrower_inst.rect.x += self.flamethrower_inst.speed
            if self.flamethrower_inst.rect.x >= width - 100:
                # Set shooting_magic_ball to False when the ball leaves the screen
                self.flamethrower_activate = False
        
        elif self.flamethrower_L:
            if round(self.flame_frames) == len(self.flame_left_list)-1 and not self.flamethrower_activate:
                self.flamethrower_inst.rect.x = self.center[0] - self.offset_x - 200
                self.flamethrower_inst.rect.y= self.center[1] - self.offset_y - 105
                self.flamethrower_activate = True

            if self.flamethrower_activate and self.flamethrower_L:
                self.flamethrower_inst.flamethrower_animation(self.screen,False,True)
                self.flamethrower_inst.rect.x -= self.flamethrower_inst.speed
            if self.flamethrower_inst.rect.x <=-100 :
                self.flamethrower_activate = False

    #left and right flamethrower attack is used to give logic to the fireball attack
    def flamethrower_attack_R(self):
        if self.flamethrower_R:
            if self.flamethrower_animate and not self.flamethrower_activate and self.is_facing_R:
                self.flame_frames += .09
                if self.flame_frames >= len(self.flame_right_list):
                    self.flame_frames = 0
                    self.flamethrower_animate = False
                self.image = self.flame_right_list[int(self.flame_frames)]
        pass
    def flamethrower_attack_L(self):
        if self.flamethrower_L:
            if self.flamethrower_animate and not self.flamethrower_activate and self.is_facing_L:
                self.flame_frames += .09
                if self.flame_frames >= len(self.flame_left_list):
                    self.flame_frames = 0
                    self.flamethrower_animate = False
                self.image = self.flame_left_list[int(self.flame_frames)]

        pass

    
    #Here we control the energy of the attacks and give the energy variable more logic
    def energy_consumption(self):
        if self.energy < 10:
            self.is_attacking_R,self.is_attacking_L = False,False
        if self.energy < 20:
            self.flamethrower_R,self.flamethrower_L = False,False
        if self.energy < 15:
            self.is_blocking_R,self.is_blocking_L = False,False
        if self.energy < 20:
            self.is_teloporting = False
        if self.energy < 0:
            self.energy = 0 
            
    #blocking left and right just summon force fields that rely on the energy and hp of shield
    def blocking_right(self):
        if self.is_blocking_R and self.is_facing_R and self.shield_hp > 0:
            self.energy -= .6
            self.image = self.block_R_img
        
        if self.shield_hp <= 0:
            self.image = self.magic_attack_R_list[0]
            self.shield_hp += .5
        
        if self.energy < 10:
            self.image = self.magic_attack_R_list[0]
            pass

    def blocking_left(self):
        if self.is_blocking_L and self.is_facing_L and self.shield_hp > 0:
            self.energy -= .6
            self.image = self.block_L_img


        if self.shield_hp <= 0:
            self.image = self.magic_attack_L_list[0]
            self.shield_hp += .5

        if self.energy < 10:
            self.image = self.magic_attack_L_list[0]



     #this function is used for controlling the attacks and other motions   
    def key_down(self, keys):
        
        if keys[pygame.K_d]:
            self.is_walking_R = True
            self.is_facing_R = True
            self.is_walking_L = False
            self.is_facing_L = False
        elif keys[pygame.K_a]:
            self.is_walking_L = True
            self.is_facing_L = True
            self.is_facing_R = False
            self.is_walking_R = False
        if keys[pygame.K_w]:
            self.is_in_air = True

        if keys[pygame.K_1]:
            if self.is_facing_R:
                self.is_attacking_R = True
                self.attack_animation = True
                self.is_attacking_L = False
                self.is_facing_L = False
            elif self.is_facing_L:
                self.is_facing_R = False
                self.is_attacking_L = True
                self.attack_animation = True
                self.is_attacking_R = False
        
        if keys[pygame.K_2]:
            if self.is_facing_R:
                self.flamethrower_R = True
                self.flamethrower_animate = True
                self.flamethrower_L = False
                self.is_facing_L = False
            elif self.is_facing_L:
                self.is_facing_R = False
                self.flamethrower_L = True
                self.flamethrower_animate = True
                self.flamethrower_R = False
        
        if keys[pygame.K_q]:
            if self.is_facing_R:
                self.is_blocking_R = True
                self.is_blocking_L = False
            elif self.is_facing_L:
                self.is_blocking_L = True
                self.is_blocking_R = False

               
    #used to control animmations also
    def key_up(self, event):
        if event.key == pygame.K_d:
            self.is_walking_R = False
            #self.is_facing_L = False
        elif event.key == pygame.K_a:
            self.is_walking_L = False
            #self.is_facing_R = False
        elif event.key == pygame.K_q:
            self.is_blocking_L = False
            self.is_blocking_R = False
            if self.is_facing_R:
                self.image = self.magic_attack_R_list[0]
            elif self.is_facing_L:
                self.image = self.magic_attack_L_list[0]

    #draws every frame and is used in the main game loop
    def update(self,width,height):
        if self.flamethrower_activate and self.main_mens.is_music:
            fireball_sound =  mixer.Sound("sound folder/flamethrower_jasper_sound.mp3")
            fireball_sound.play()
        if self.shooting_magic_ball and self.main_mens.is_music:
            laser_sound = mixer.Sound("sound folder/beemed.mp3")
            laser_sound.play()
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    mouse = mouse_x,mouse_y

        keys = pygame.key.get_pressed()
        self.key_down(keys)
        self.walking()
        self.jumping()
        self.drawing_magic_ball(width)
        self.drawing_flamethrower(width)
        self.energy_consumption()
        self.energy_management()
        self.get_state()

        if self.is_attacking_R:
            self.attacking_right()
        elif self.is_attacking_L:
            self.attacking_left()
        
        if self.is_blocking_R:
            self.blocking_right()
        elif self.is_blocking_L:
            self.blocking_left()


        if self.flamethrower_R:
            self.flamethrower_attack_R()
        elif self.flamethrower_L:
            self.flamethrower_attack_L()
        self.center = (self.rect.x + self.rect.width // 2, self.rect.y + self.rect.height // 2)

        self.screen.blit
        if self.is_facing_L:
            self.screen.blit(self.image,(self.rect.x - 50,self.rect.y))
        else:
            self.screen.blit(self.image,self.rect)
        

            # Draw health bar
        pygame.draw.rect(self.screen, self.red, (0, 30, 200, 25))
        pygame.draw.rect(self.screen, self.green, (0, 30, self.hp, 25))
        self.screen.blit(self.health_text, (0, 30))

        # Draw energy bar
        pygame.draw.rect(self.screen, self.white, (0, 70, 200, 15))
        pygame.draw.rect(self.screen, self.blue, (0, 70, self.energy, 15))
        self.screen.blit(self.energy_text, (0, 70))
    
        #gravity and logic checking
        if self.rect.x >= width - 25:
            self.rect.x - 100

        
        if self.rect.x <= 0:
            self.rect.x + 100

                
    
        if not self.is_in_air:
            self.rect.y = self.y

        #pygame.draw.rect(self.screen,self.green,self.magic_ball.rect)
        