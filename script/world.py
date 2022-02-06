import pygame as pg
import noise
import random
from camera import Camera
from tiles import RockTile, Tile, TreeTile
from settings import TILE_SIZE
from utils import ImageContainer, cart_to_iso, draw_text, iso_to_cart


class World:
    def __init__(self, screen, grid_length_x, grid_length_y, width, height, hud) -> None:
        self.grid_x = grid_length_x
        self.grid_y = grid_length_y
        self.width = width
        self.height = height
        self.screen = screen
        self.hud = hud

        self.block_image = pg.image.load("../images/block.png").convert_alpha()
        self.perlin_scale = grid_length_x / 2
                
        # case 1
        # surface rendering the tiles in that area
        # we double the tile size and grid length because in isometric pos like 128x64
        self.block_tiles = pg.Surface((grid_length_x * TILE_SIZE * 2 + TILE_SIZE / 3, 
                                       grid_length_y * TILE_SIZE + TILE_SIZE * 2 + TILE_SIZE / 2)).convert_alpha()
        self.world_tiles = self.create_world()

        self.camera = Camera(width, height)

        self.temp_tile = None

    def create_world(self):
        # Creates grid object then stores the objects
        world_tiles = []
        for x in range(self.grid_x):
            world_tiles.append([])
            for y in range(self.grid_y):

                tile = self.create_grid(x, y)
                world_tiles[x].append(tile)
                # case 2
                # some of tiles will be rendered in negative positions, and due to the fact that the surface doesn't take 
                # negative values, we will use the half of the grass surface as offset in order to render the block tiles
                render_pos = tile.render_pos
                self.block_tiles.blit(self.block_image,
                                    (render_pos[0] + self.block_tiles.get_width()/2,
                                    render_pos[1]))

        return world_tiles
    
    def create_grid(self, grid_x, grid_y):
        # Creates Tile object and return 
        # 1- 64x64 Grid
        # 2- 64x64 Grid with aligned offsets on X axes
        # 3- 64x64 Grid with aligned offsets on both axes 
        # 4- 64x64 Grid with aligned offsets on Y axes
        rect = [
            (grid_x * TILE_SIZE, grid_y * TILE_SIZE), 
            (grid_x * TILE_SIZE + TILE_SIZE, grid_y * TILE_SIZE),
            (grid_x * TILE_SIZE + TILE_SIZE, grid_y * TILE_SIZE + TILE_SIZE),
            (grid_x * TILE_SIZE, grid_y * TILE_SIZE + TILE_SIZE)]

        # convert cartesan pos to isometric pos
        iso_poly = [cart_to_iso(x, y) for x, y in rect]
        
        # to get the left corner of isometric pos in order to draw the image properly,
        # which requries to get min values of x and y axes
        min_x = min([x for x, y in iso_poly])
        min_y = min([y for x, y in iso_poly])
                
        # generates two dimensional values
        perlin = 100 * noise.pnoise2(grid_x/self.perlin_scale, 
                                     grid_y/self.perlin_scale) 
        r = random.randint(1, 100)
        if perlin >= 15 or perlin <= -35:
            tile = TreeTile(grid_x, grid_y, rect, iso_poly, [min_x, min_y])
        else:
            if r <= 5:
                tile = TreeTile(grid_x, grid_y, rect, iso_poly, [min_x, min_y])
            elif r <= 10:
                tile = RockTile(grid_x, grid_y, rect, iso_poly, [min_x, min_y])
            else:
                tile = Tile(grid_x, grid_y, rect, iso_poly, [min_x, min_y])

        return tile

    def update(self):
        # updates camera's positions
        self.camera.update()
        mouse_pos = pg.mouse.get_pos()
        self.temp_tile = None

        if self.hud.selected_tile != None:
            grid_pos = self.mouse_to_grid(mouse_pos[0], mouse_pos[1], self.camera.scroll)
            if self.hud.can_place_tile(grid_pos):
                img = self.hud.selected_tile.image.copy()
                img.set_alpha(100)
                render_pos = self.world_tiles[grid_pos[0]][grid_pos[1]].render_pos
                self.temp_tile = Tile(image=img, render_pos=render_pos)

    def draw(self):

        # Draw Tile (block) and add offset to the render position to center the tile as batch
        # so that it would not allocate the memory a lot
        self.screen.blit(self.block_tiles, (self.camera.scroll.x, self.camera.scroll.y))
        
        for x in range(self.grid_x):
            for y in range(self.grid_y):
                
                # Draw rectangular
                # cart_grid_pos = self.world_tiles[x][y].cart_rect
                # rect = pg.Rect(cart_grid_pos[0][0], cart_grid_pos[0][1], TILE_SIZE, TILE_SIZE)
                # pg.draw.rect(self.screen, (255, 0, 0), rect, 1)

                # Draw block image
                # self.screen.blit(block_image, 
                #                (render_pos[0] + self.width/2,
                #                 render_pos[1] + self.height/4))
                
                render_pos = self.world_tiles[x][y].render_pos
                # Draw polygon
                p = self.world_tiles[x][y].iso_poly
                # Add offset the positions
                p = [(x + self.block_tiles.get_width()/2 + self.camera.scroll.x, y + self.camera.scroll.y) for x, y in p]
                pg.draw.polygon(self.screen, (0, 255, 0), p, 1)

                # Draw trees and stones randomly using perlin noise
                # If the tiles exceed the threshold of block tiles you should extract y axes from difference height between image and tile
                # due to this reason the screen will start rendering plus offset position but not in the middle of the screen
                if self.world_tiles[x][y].tile_name != "block":
                    self.screen.blit(self.world_tiles[x][y].image, 
                                    (render_pos[0] + self.block_tiles.get_width()/2 + self.camera.scroll.x,
                                     render_pos[1] - (self.world_tiles[x][y].image.get_height() - TILE_SIZE) + self.camera.scroll.y))

                
                # Draw temporary tile on the screen
                if self.temp_tile != None:
                    tem_pos = self.temp_tile.render_pos
                    self.screen.blit(self.temp_tile.image,
                                    (tem_pos[0] + self.block_tiles.get_width() / 2 + self.camera.scroll.x,
                                    tem_pos[1] - (self.temp_tile.image.get_height() - TILE_SIZE) + self.camera.scroll.y))
            
                # font = pg.font.SysFont('arial', 50)
                # text = font.render("1", True, (0, 0, 0)).convert_alpha()
                # self.screen.blit(text,
                #                 (render_pos[0] + self.block_tiles.get_width()/2 + self.camera.scroll.x,
                #                  render_pos[1] + self.camera.scroll.y))

    def mouse_to_grid(self, x, y, scroll):
        # transform world position removing the camera scroll and offsets
        world_x = x - scroll.x - self.block_tiles.get_width()/2
        world_y = y - scroll.y

        cart_x, cart_y = iso_to_cart(world_x, world_y)

        grid_x = int(cart_x // TILE_SIZE)
        grid_y = int(cart_y // TILE_SIZE)

        return grid_x, grid_y