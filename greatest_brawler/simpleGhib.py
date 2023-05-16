
import pygame

# Simplified Ghibs class
class SimpleGhibs(pygame.sprite.Sprite):
    def __init__(self, screen, x, y):
        super().__init__()
        self.screen = screen
        self.x = x
        self.y = y
        self.image = pygame.image.load("walking_swordsman/brawl_swordsman_walking.png")
        self.rect = self.image.get_rect()

        # Walking animations
        self.ghibs_walking_right_list = []
        self.ghibs_walking_left_list = []
        self.ghibs_walking_right = pygame.image.load("walking_swordsman/brawl_swordsman_walking.png")
        self.ghibs_walking_right = pygame.image.load("walking_swordsman/walking_img_swordsman.png")
        for image in self.ghibs_walking_right_list:
            flipped_image = pygame.transform.flip(image, True, False)
            self.ghibs_walking_left_list.append(flipped_image)

    def update(self, screen):
        screen.blit(self.image, (self.x, self.y))

