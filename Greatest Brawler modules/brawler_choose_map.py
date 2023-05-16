import pygame

class Map(object):
    def __init__(self,screen,x,y,width,height):
        super().__init__()
        self.selected_map = None
        self.get_map_screen = pygame.image.load("brawler_map_picker_screen.png")
        self.night_sky_map = pygame.image.load("brawler_maps/greatest_brawler_map_1.png")
        self.brawling_winter_map = pygame.image.load("brawling_out.png")
        self.width = width
        self.height = height
        self.screen = screen
        self.map_screen = True
        self.x = x
        self.y = y
        
        
        #coordinates for the map
        self.night_sky_x = (50,261)
        self.night_sky_y = (90,300)
        self.night_sky = (self.night_sky_x,self.night_sky_y)
        
        self.brawling_winter_x = (370,610)
        self.brawling_winter_y = (85,327)
        self.brawling_winter = (self.brawling_winter_x,self.brawling_winter_y)


        self.map_dict = {"night sky": [self.night_sky_map,False],
                         "brawling winter": [self.brawling_winter_map,False]}


    def map_get_picked(self,events):
        for event in events:
            if event.type == pygame.QUIT:
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.mouse_x, self.mouse_y = pygame.mouse.get_pos()
                    #check if the player clicks on a option
                if self.night_sky_x[0] <= self.mouse_x <= self.night_sky_x[1] and self.night_sky_y[0] <= self.mouse_y <= self.night_sky_y[1]:
                    self.map_dict["night sky"][1] = True
                if self.brawling_winter_x[0] <= self.mouse_x <= self.brawling_winter_x[1] and self.brawling_winter_y[0] <= self.mouse_y <= self.brawling_winter_y[1]:
                    self.map_dict["brawling winter"][1] = True
                    
        self.screen.blit(self.get_map_screen,(self.x,self.y))
        
        
    def update(self,screen):
        events = pygame.event.get()
        self.map_get_picked(events)
    
        for maps, (map_key, map_bool) in self.map_dict.items():
            if map_bool:
                self.selected_map = map_key
                self.screen.blit(map_key, (self.x, self.y))
                print(map_key)
                break