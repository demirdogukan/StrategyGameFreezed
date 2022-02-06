import pygame as pg


class Tile:
    def __init__(self, pos_x=0, pos_y=0, cart_rect=0, iso_poly=0, render_pos=0, tile_name="block", image=None):
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.cart_rect = cart_rect
        self.iso_poly = iso_poly
        self.render_pos = render_pos
        self.tile_name = tile_name
        self.image = image


class TreeTile(Tile):
    def __init__(self, pos_x, pos_y, cart_rect, iso_poly, render_pos):
        super().__init__(pos_x, pos_y, cart_rect, iso_poly, render_pos, tile_name="tree")
        self.image = pg.image.load("../images/tree.png").convert_alpha()


class RockTile(Tile):
    def __init__(self, pos_x, pos_y, cart_rect, iso_poly, render_pos):
        super().__init__(pos_x, pos_y, cart_rect, iso_poly, render_pos, tile_name="rock")
        self.image = pg.image.load("../images/rock.png").convert_alpha()


class ImageIcon:
    def __init__(self, name, icon, image, rect) -> None:
        self.name = name
        self.icon = icon
        self.image = image
        self.rect  = rect

    