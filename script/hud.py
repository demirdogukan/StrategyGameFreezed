import pygame as pg
from tiles import ImageIcon
from utils import ImageContainer, draw_text, scale_image


class Hud:
    def __init__(self, screen, width, height, grid_length_x, grid_length_y):
        self.width = width
        self.height = height
        self.screen = screen
        self.grid_length_x = grid_length_x
        self.grid_length_y = grid_length_y

        self.hud_color = (198, 155, 93, 175)

        # hash map that stores images
        self.image_container = ImageContainer.get_container()

        # resources  hud
        self.resources_surface = pg.Surface((width, height * 0.02), pg.SRCALPHA)
        self.resources_rect = self.resources_surface.get_rect(topleft=(0, 0))
        self.resources_surface.fill(self.hud_color)

        # building hud
        self.building_surface = pg.Surface((width * 0.15, height * 0.25), pg.SRCALPHA)
        self.building_rect = self.building_surface.get_rect(topleft=(self.width * 0.84, self.height * 0.74))
        self.building_surface.fill(self.hud_color)

        # select hud
        self.select_surface = pg.Surface((width * 0.3, height * 0.25), pg.SRCALPHA)
        self.select_rect = self.select_surface.get_rect(topleft=(self.width * 0.35, self.height * 0.74))
        self.select_surface.fill(self.hud_color)

        self.hud_images = self.create_building_hud()

        self.selected_tile = None
    
    def draw(self):
        #if self.selected_tile != None:
        #    self.screen.blit(self.selected_tile, 
        #                    (pg.mouse.get_pos()[0] - self.selected_tile.get_width() / 2,
        #                     pg.mouse.get_pos()[1] - self.selected_tile.get_height() / 2))
        
        # Draws panels
        self.screen.blit(self.resources_surface, (0, 0))
        self.screen.blit(self.building_surface, (self.width * 0.84, self.height * 0.74))
        self.screen.blit(self.select_surface, (self.width * 0.35, self.height * 0.74))
    
        for image in self.hud_images:
            self.screen.blit(image.icon, (image.rect))

        # Draws Resources Texts
        text_pos = self.width - 400
        for i in ["Woods:", "Gold:", "Stone:"]:
            draw_text(self.screen, i, 26, (255, 255, 255), (text_pos, 0))
            text_pos += 100

    def update(self):
        mouse_pos = pg.mouse.get_pos()
        mouse_action = pg.mouse.get_pressed()

        if mouse_action[2]: self.selected_tile = None

        for img in self.hud_images:
            if img.rect.collidepoint(mouse_pos):
                if mouse_action[0]:
                    self.selected_tile = img

    def create_building_hud(self):
        render_pos = [self.width * 0.84 + 10, self.height * 0.74 + 10]
        object_width = self.building_surface.get_width() // 5

        tiles = []

        for name, image in self.image_container.items():
            pos_tmp = render_pos.copy()
            image_tmp = image.copy()
            scaled_image = scale_image(image_tmp, width=object_width)
            rect = scaled_image.get_rect(topleft=pos_tmp)
            
            tiles.append(ImageIcon(name, 
                        scaled_image, 
                        image, 
                        rect))
            
            render_pos[0] += scaled_image.get_width() + 10
        return tiles


    def can_place_tile(self, grid_pos):
        mouse_on_panel = False
        # checks whether it collides with panels
        for rect in [self.building_rect, self.select_rect, self.resources_rect]:
            if rect.collidepoint(pg.mouse.get_pos()):
                mouse_on_panel = True
        
        # checks whether it exceed the bounds of grids
        world_bounds = (0 <= grid_pos[0] <= self.grid_length_x) and (0 <= grid_pos[1] <= self.grid_length_y)

        return not mouse_on_panel and world_bounds
                    
         