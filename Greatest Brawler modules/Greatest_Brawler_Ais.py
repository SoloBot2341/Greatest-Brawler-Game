import pygame
import random
from pygame import mixer

from Greatest_brawler_ghibs import Ghibs
from jasper_brawler import Jasper
from jasper_brawler import Magic_ball
from jasper_brawler import flamethrower



class AIGhibs(Ghibs):
    def __init__(self,screen, x, y,hp,energy):
        super().__init__(x, y, hp,energy)  #  X: Any, y: Any, hp: Any, energy: Any) -> Noenemy
        self.screen = screen
        self.x = x
        self.y = y
        self.is_facing_R  = False
        self.is_facing_L = True
        self.action = False
        self.cooldown = 0
        self.action_delay = 200
        self.action_counter = 0
        self.shield_hp = 200
        self.hp = 200
        #basic logic for left and right
        if self.is_facing_R:
            self.image = self.walking_R_list[0]
        elif self.is_facing_L:
            self.image = self.walking_L_list[0]
        self.base_img = self.walking_R_list[0]

        #stores the choice
        self.choice = []
        self.enemy_choice_attacking = (0,1,2,3,4,2,1,0,0,2,1,3,3)
        self.enemy_choice_defending = (3,0,4,4,4,2,1,3,2,1,0,2,3,3)

    


    def blocking_right_ai(self):
        if self.is_facing_R and self.is_blocking_R and self.shield_hp > 0 and self.energy > 20:
            self.image = self.blocking_img_R
            if self.image == self.blocking_img_R:
                self.energy -= .5
        if self.shield_hp <= 0:
            self.shield_hp += 1
        
        if self.shield_hp <= 0:
            self.image = self.walking_R_list[0]
            self.is_blocking_R = False

    def blocking_left_ai(self):
        if self.is_facing_L and self.is_blocking_L and self.shield_hp > 0 and self.energy > 20:
            self.image = self.blocking_img_L
            if self.image == self.blocking_img_L:
                self.energy -= .5
        if self.shield_hp <= 0:
            self.shield_hp += 1

        if self.shield_hp <= 0:
            self.image = self.walking_L_list[0]
            self.is_blocking_L = False


    def enemies_movement_map(self,enemy):
        if self.cooldown == 10 and self.action == False:
            if enemy.state_map["Attacking?"]:
                self.choice.append(random.choice(self.enemy_choice_attacking))
            elif enemy.state_map["Defending?"]:
                self.choice.append(random.choice(self.enemy_choice_defending))
            elif enemy.state_map["Jumping?"]:
                self.choice.append(3)
            elif enemy.state_map["Chasing?"]:
                self.choice.append(random.choice(self.enemy_choice_defending))

        if len(self.choice) == 3:
            self.choice.remove(-1)
        
          
    def Ai_movement_map(self,enemy):
        if self.action == True:
            if self.choice:
                if self.choice[0] == 0 and enemy.rect.x > self.rect.x:
                    self.rect.x += self.walk_sped
                    self.is_walking_R = True
                    self.is_facing_R = True
                    self.is_facing_L= False
                    self.is_walking_L = False
                    self.walk_right()
                #walking left
                elif self.choice[0] == 0 and enemy.rect.x < self.rect.x:
                    self.rect.x -= self.walk_sped
                    self.is_facing_L = True
                    self.is_walking_L = True
                    self.is_walking_R = False
                    self.is_facing_R = False
                    self.walk_left()

                #blocking right
                if self.choice[0] == 1  and enemy.rect.x > self.rect.x:
                    self.is_facing_R = True
                    self.is_facing_L = False
                    if self.is_facing_R and not self.is_facing_L:
                        self.is_blocking_R = True
                        if self.is_blocking_R:
                            self.blocking_right_ai()
                #blocking left
                elif self.choice[0] == 1 and enemy.rect.x < self.rect.x:
                    self.is_facing_L = True
                    self.is_facing_R = False
                    if self.is_facing_L and not self.is_facing_R:
                        self.is_blocking_L = True
                        if self.is_blocking_L:
                            self.blocking_left_ai()

                if self.choice[0] == 3 and self.is_facing_R and not self.is_facing_L and enemy.rect.x == self.rect.x:
                    self.is_attacking_R = True
                    self.is_attacking_L = False
                    self.attacking_right()
                #attacking left
                elif self.choice[0] == 3 and self.is_facing_L and not self.is_facing_R and enemy.rect.x == self.rect.x:
                    self.is_attacking_L = True
                    self.is_attacking_R = False
                    self.attacking_left()

                    if self.rect.x != enemy.rect.x:
                        self.choice[0] = 0


                if self.choice[0] == 2 and self.is_facing_R and not self.is_facing_L:
                    self.is_jumping_R = True
                    self.is_jumping_L = False
                    self.is_in_air = True
                    self.jumping_right()
                    self.action_counter - 110

                elif self.choice[0] == 2 and self.is_facing_L and not self.is_facing_R:
                    self.is_jumping_R = False
                    self.is_jumping_L = True
                    self.is_in_air = True
                    self.jumping_left()
                    self.action_counter - 110
                
                if self.choice[0] == 4 and self.is_facing_R and not self.is_facing_L and enemy.rect.x == self.rect.x:
                    self.is_impact_R = True
                    self.is_impact_L = False
                    self.impact_attack_right()
                #impact attacking left
                elif self.choice[0] == 4 and self.is_facing_L and not self.is_facing_R and enemy.rect.x == self.rect.x:
                    self.is_impact_R = False
                    self.is_impact_L = True
                    self.impact_attack_left()

                    if self.rect.x != enemy.rect.x:
                        self.choice[0] = 0
                    
                if self.rect.x == enemy.rect.x:
                    self.choice[0] = random.choice(range(3,5))
                
        

            else:  # If list is empty
                self.is_walking_L = False
                self.is_walking_R = False
                self.is_blocking_L = False
                self.is_blocking_R = False
    
    
    def collisions_ai_ghibs(self,enemy):
        if self.is_attacking_R or self.is_attacking_L:
            if self.rect.colliderect(enemy.rect):
                enemy.hp -= .3
        elif self.is_impact_R or self.is_impact_L:
            if self.rect.colliderect(enemy.rect):
                enemy.hp -= .8
                
        elif enemy.is_blocking_L or enemy.is_blocking_R:
            if self.rect.colliderect(enemy.rect):
                enemy.shield_hp -= 7

    #ghibs update function
    def update(self, enemy,screen):
        sword_swing_sound = mixer.Sound("sound folder/ghib slash sound.mp3")
        if self.main_men.is_music:
            if self.is_attacking_R:
                sword_swing_sound.play()
            if self.is_attacking_L:
                sword_swing_sound.play()
            if self.is_impact_attack_finished:
                sword_swing_sound.play()
   

        self.enemies_movement_map(enemy)
        self.Ai_movement_map(enemy)
        self.energy_management()
        self.collisions_ai_ghibs(enemy)

        self.screen.blit(self.image, self.rect)

        if self.is_in_air and self.is_facing_L:
            self.jumping_left()
        elif self.is_facing_R and self.is_in_air:
            self.jumping_right()



        #draw the health bar
        pygame.draw.rect(self.screen, self.red, (490, 25, 200, 25))
        pygame.draw.rect(self.screen, self.green, (490, 25, self.hp, 25))
        self.screen.blit(self.health_text, (490, 25))

        # Draw energy bar
        pygame.draw.rect(self.screen, self.white, (490, 65, 200, 20))
        pygame.draw.rect(self.screen, self.blue, (490, 65, self.energy, 20))
        self.screen.blit(self.energy_text, (490, 65))

        if self.choice == []:
            self.action = False
        elif self.choice != []:
            self.action = True
        
        if self.cooldown < 11:
            self.cooldown += 1
        if self.cooldown >= 11 and self.action == False:
            self.cooldown = 0

        if self.action:
            self.action_counter += 1
            if self.action_counter >= self.action_delay:
                self.action = False
                self.action_counter = 0

        if self.action_counter >= self.action_delay - 1:
            self.choice = []

                #gravity and logic checking
        if self.rect.x >= 700- 50:
            walking_right = False
            self.rect.x -= 50
        
        if self.rect.x <= 0:
            walking_left = False
            self.rect.x += 50
                
    
        if not self.is_in_air:
            self.rect.y = self.y

            
        


#jasper ai class
class AIJasper(Jasper):
    def __init__(self, screen, x, y,hp, energy):
        super().__init__(screen, x, y,hp,energy)
        self.screen = screen
        self.x = x
        self.y = y
        self.base_img = self.magic_attack_R_list[0]

        #bools 
        self.is_facing_R  = False
        self.is_facing_L = True
        self.action = False
        self.fire_blast_R = False
        self.fire_blast_L = False
        self.force_ball_R = False
        self.force_ball_L = False
        self.drawing_fire_blast = False
        self.drawing_force_ball = False
        self.attack_animation_ai = False
        self.frames_speed = 0
        self.fire_frames = 0
        self.is_flames_animating = False

        #timers and stats
        self.cooldown = 0
        self.action_delay = 200
        self.action_counter = 0
        self.shield_hp = 200
        self.hp = 200


        
        #loading up instances will need
        self.force_ball = Magic_ball(self.center[0] - self.offset_x,self.center[1] - self.offset_y,1)
        self.fire_blast_inst = flamethrower(self.center[0] - self.offset_x,self.center[1] - self.offset_y - 105,.5)

        #decided to change the image name for easier maintainability
        self.blocking_img_R = self.block_R_img
        self.blocking_img_L = self.block_L_img

        #basic logic for left and right
        if self.is_facing_R:
            self.image = self.magic_attack_R_list[0]
        elif self.is_facing_L:
            self.image = self.magic_attack_L_list[0]

        #stores the choice
        self.choice = []
        self.enemy_choice_attacking = (4,1,2,3,4,4,4,4,4,3,3,3,1,1,1,1,0,0,0,0,0,0,2) #0 walking, 1 blocking, 2 jumoing
        self.enemy_choice_defending = (3,0,4,3,3,4,1,4,4,2,1,2,3,4,4,1,0,0,0,1,2,4,3) # 3 attack,4special


    #remade some functions from the jasper class

    def drawing_ball(self,width):
        if self.is_attacking_R:
            if round(self.frames_speed) == len(self.magic_attack_R_list)-1 and not self.drawing_force_ball:
                # Update the position of the magic ball right when the attack is initiated
                self.force_ball.rect.x = self.center[0] - self.offset_x
                self.force_ball.rect.y = self.center[1] - self.offset_y
                self.drawing_force_ball = True

            if self.drawing_force_ball and self.is_attacking_R:
                self.screen.blit(self.force_ball.image,self.force_ball.rect)
                self.force_ball.rect.x += self.force_ball.speed

            if self.force_ball.rect.x >= width + 100 :
                # Set drawing_force_ball to False when the ball leaves the screen\
                self.drawing_force_ball = False

        elif self.is_attacking_L:
            if round(self.frames_speed) == len(self.magic_attack_R_list)-1 and not self.drawing_force_ball:
                self.force_ball.rect.x = self.center[0] - self.offset_x - 200
                self.force_ball.rect.y = self.center[1] - self.offset_y
                self.drawing_force_ball = True

            if self.drawing_force_ball and self.is_attacking_L:
                self.screen.blit(self.force_ball.image,self.force_ball.rect)
                self.force_ball.rect.x -= self.force_ball.speed

            
            if self.force_ball.rect.x <=-100:
                self.drawing_force_ball = False


    def attacking_right(self):
        if self.is_attacking_R:
            if self.attack_animation_ai and not self.drawing_force_ball and self.is_facing_R:
                self.frames_speed += .9
                if self.frames_speed >= len(self.magic_attack_R_list):
                    self.frames_speed = 0
                    self.attack_animation_ai = False
                self.image = self.magic_attack_R_list[int(self.frames_speed)]
    

    #this function is the basic attack for the left side
    def attacking_left(self):
        if self.is_attacking_L:
            if self.attack_animation_ai and not self.drawing_force_ball and self.is_facing_L:
                self.frames_speed += .9
                if self.frames_speed >= len(self.magic_attack_L_list):
                    self.frames_speed = 0
                    self.attack_animation = False
                self.image = self.magic_attack_L_list[int(self.frames_speed)]

        #this function draws the fire ball image
   
   
   
    def fire_blast_drawing(self,width):
        if self.fire_blast_R:
            if round(self.fire_frames) == len(self.flame_right_list)-1 and not self.drawing_fire_blast:
                # Update the position of the magic ball right when the attack is initiated
                self.fire_blast_inst.rect.x = self.center[0] - self.offset_x
                self.fire_blast_inst.rect.y= self.center[1] - self.offset_y - 105
                self.drawing_fire_blast = True

            if self.drawing_fire_blast and self.fire_blast_R:
                self.fire_blast_inst.flamethrower_animation(self.screen,True,False)
                self.fire_blast_inst.rect.x += self.fire_blast_inst.speed
            if self.fire_blast_inst.rect.x >= width + 50:
                # Set shooting_magic_ball to False when the ball leaves the screen
                self.drawing_fire_blast = False
        
        elif self.fire_blast_L:
            if round(self.fire_frames) == len(self.flame_left_list)-1 and not self.drawing_fire_blast:
                self.fire_blast_inst.rect.x = self.center[0] - self.offset_x - 200
                self.fire_blast_inst.rect.y= self.center[1] - self.offset_y - 105
                self.drawing_fire_blast = True

            if self.drawing_fire_blast and self.fire_blast_L:
                self.fire_blast_inst.flamethrower_animation(self.screen,False,True)
                self.fire_blast_inst.rect.x -= self.fire_blast_inst.speed
            if self.fire_blast_inst.rect.x <=-100 :
                self.drawing_fire_blast = False

    #left and right flamethrower attack is used to give logic to the fireball attack
    def fireblast_attack_R(self):
        if self.fire_blast_R:
            if self.is_flames_animating and not self.drawing_fire_blast and self.is_facing_R:
                self.fire_frames += .09
                if self.fire_frames >= len(self.flame_right_list):
                    self.fire_frames = 0
                    self.is_flames_animating = False
                self.image = self.flame_right_list[int(self.fire_frames)]
        pass
    def fireblast_attack_L(self):
        if self.fire_blast_L:
            if self.is_flames_animating and not self.drawing_fire_blast and self.is_facing_L:
                self.fire_frames += .09
                if self.fire_frames >= len(self.flame_left_list):
                    self.fire_frames = 0
                    self.is_flames_animating = False
                self.image = self.flame_left_list[int(self.fire_frames)]

        pass




    def blocking_right_ai(self):
        if self.is_facing_R and self.is_blocking_R and self.shield_hp > 0 and self.energy > 20:
            self.image = self.blocking_img_R
            if self.image == self.blocking_img_R:
                self.energy -= 5
        if self.shield_hp <= 0:
            self.shield_hp += .3
        
        if self.shield_hp <= 0 or self.energy <= 20:
            self.image = self.magic_attack_R_list[0]
            self.is_blocking_R = False

    def blocking_left_ai(self):
        if self.is_facing_L and self.is_blocking_L and self.shield_hp > 0 and self.energy > 20:
            self.image = self.blocking_img_L
            if self.image == self.blocking_img_L:
                self.energy -= 5

        if self.shield_hp <= 0:
            self.shield_hp += .3


        if self.shield_hp <= 0:
            self.image = self.magic_attack_L_list[0]
            self.is_blocking_L = False


    def enemies_movement_map(self,enemy):
        if self.cooldown == 10 and self.action == False:
            if enemy.state_map["Attacking?"]:
                self.choice.append(random.choice(self.enemy_choice_attacking))
            elif enemy.state_map["Defending?"]:
                self.choice.append(random.choice(self.enemy_choice_defending))
            elif enemy.state_map["Jumping?"]:
                self.choice.append(3)
            elif enemy.state_map["Chasing?"]:
                self.choice.append(random.choice(self.enemy_choice_defending))

        if len(self.choice) == 3:
            del(self.choice[-1])
        
          
    def Ai_movement_map(self,enemy):
        if self.action == True:
            if self.choice:
                if self.choice[0] == 0 and self.rect.x <= enemy.rect.x + 550:
                    self.is_walking_R = True
                    self.is_facing_R = True
                    self.is_facing_L= False
                    self.is_walking_L = False
                    if self.rect.x <= enemy.rect.x + 550:
                        self.choice[0] = random.choice((3,4,1,2))



                #walking left
                elif self.choice[0] == 0 and self.rect.x >= enemy.rect.x - 550:
                    self.is_facing_L = True
                    self.is_walking_L = True
                    self.is_walking_R = False
                    self.is_facing_R = False
                    if self.rect.x >= enemy.rect.x + 550:
                        self.choice[0] = random.choice((3,4,1,2))

                #blocking right
                if self.choice[0] == 1:
                    self.is_facing_R = True
                    self.is_facing_L = False
                    if self.is_facing_R and not self.is_facing_L:
                        self.is_blocking_R = True
                        if self.is_blocking_R:
                            self.blocking_right_ai()
                #blocking left
                elif self.choice[0] == 1:
                    self.is_facing_L = True
                    self.is_facing_R = False
                    if self.is_facing_L and not self.is_facing_R:
                        self.is_blocking_L = True
                        if self.is_blocking_L:
                            self.blocking_left_ai()

                if self.choice[0] == 3 and self.is_facing_R and not self.is_facing_L:
                    self.is_attacking_R = True
                    self.is_attacking_L = False

                #attacking left
                elif self.choice[0] == 3 and self.is_facing_L and not self.is_facing_R:
                    self.is_attacking_L = True
                    self.is_attacking_R = False
                    

                if self.choice[0] == 2 and self.is_facing_R and not self.is_facing_L:
                    self.is_jumping_R = True
                    self.is_jumping_L = False
                    self.is_in_air = True
                    self.action_counter + 180

                elif self.choice[0] == 2 and self.is_facing_L and not self.is_facing_R:
                    self.is_jumping_R = False
                    self.is_jumping_L = True
                    self.is_in_air = True
                    self.action_counter + 180
                
                if self.choice[0] == 4 and self.is_facing_R and not self.is_facing_L:
                    self.fire_blast_R = True
                    self.fire_blast_L = False
   
                elif self.choice[0] == 4 and self.is_facing_L and not self.is_facing_R:
                    self.fire_blast_R = False
                    self.fire_blast_L = True
                




            else:  # If list is empty
                self.is_walking_L = False
                self.is_walking_R = False
                self.is_blocking_L = False
                self.is_blocking_R = False
                self.is_attacking_L = False
                self.is_attacking_R = False
                self.fire_blast_L = False
                self.fire_blast_R = False
                self.is_jumping_L = False
                self.is_jumping_R = False

    def collisions_ai_jaspers(self,enemy):
        ai_torch = False
        if self.drawing_force_ball:
            if self.force_ball.rect.colliderect(enemy.rect) and enemy.is_blocking_L or enemy.is_blocking_R:
                    if enemy.shield_hp > 0:
                        enemy.shield_hp -= self.force_ball.damage
                        if enemy.shield_hp < 0:
                            enemy.shield_hp = 0

        elif self.drawing_fire_blast:
            if self.fire_blast_inst.rect.colliderect(enemy.rect) and enemy.is_blocking_L or enemy.is_blocking_R:
                 if enemy.shield_hp > 0:
                        enemy.shield_hp -= self.fire_blast_inst.damage
                        if enemy.shield_hp < 0:
                            enemy.shield_hp = 0
            

        elif enemy.rect.colliderect(self.force_ball.rect):
            if self.drawing_force_ball:
                enemy.hp -= 2

        
        elif enemy.rect.colliderect(self.fire_blast_inst.rect):
            if self.drawing_fire_blast:
                ai_torch = True
                enemy.hp -= self.fire_blast_inst.damage
                if ai_torch and enemy.hp != 0:
                    enemy.hp -= .5
                if enemy.hp == 0:
                    ai_torch = False



    def update(self,enemy,screen):
        if self.flamethrower_activate and self.main_mens.is_music:
            fireball_sound =  mixer.Sound("sound folder/flamethrower_jasper_sound.mp3")
            fireball_sound.play()
        if self.shooting_magic_ball and self.main_mens.is_music:
            laser_sound = mixer.Sound("sound folder/beemed.mp3")
            laser_sound.play()
        self.enemies_movement_map(enemy)
        self.Ai_movement_map(enemy)
        self.energy_management()
        self.collisions_ai_jaspers(enemy)
        self.fire_blast_drawing(width=700)
        self.drawing_ball(width=700)
        self.energy_consumption()
    
   
        if self.is_walking_L:
            self.walking()
        elif self.is_walking_R:
            self.walking()

        if self.is_in_air:
            self.jumping()

        if self.is_attacking_R:
            self.attacking_right()
        elif self.is_attacking_L:
            self.attacking_left()

        if self.fire_blast_R:
            self.fireblast_attack_R()
        elif self.fire_blast_L:
            self.fireblast_attack_L()
        

        self.center = (self.rect.x + self.rect.width // 2, self.rect.y + self.rect.height // 2)

        self.screen.blit(self.image, self.rect)

        #draw the health bar
        pygame.draw.rect(self.screen, self.red, (490, 25, 200, 25))
        pygame.draw.rect(self.screen, self.green, (490, 25, self.hp, 25))
        self.screen.blit(self.health_text, (490, 25))

        # Draw energy bar
        pygame.draw.rect(self.screen, self.white, (490, 65, 200, 20))
        pygame.draw.rect(self.screen, self.blue, (490, 65, self.energy, 20))
        self.screen.blit(self.energy_text, (490, 65))

        if self.choice == []:
            self.action = False
        elif self.choice != []:
            self.action = True
        
        if self.cooldown < 11:
            self.cooldown += 1
        if self.cooldown >= 11 and self.action == False:
            self.cooldown = 0

        if self.action:
            self.action_counter += 1
            if self.action_counter >= self.action_delay:
                self.action = False
                self.action_counter = 0


        if self.action_counter >= self.action_delay - 1:
            self.choice = []
        
        #gravity and logic checking
        if self.rect.x >= 700 - 50:
            walking_right = False
            self.rect.x -= 100
        
        if self.rect.x <= 0:
            walking_left = False
            self.rect.x += 100
                
    
        if not self.is_in_air:
            self.rect.y = self.y


