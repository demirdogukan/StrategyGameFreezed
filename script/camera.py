from re import X
import pygame as pg


class Camera:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        
        self.speed = 25
        self.x = 0
        self.y = 0

        self.scroll = pg.Vector2(0, 0)

    def update(self):
        pos = pg.mouse.get_pos()

        if pos[0] > self.width * 0.97:
            self.x = -self.speed
        elif pos[0] < self.width * 0.03:
            self.x = self.speed
        else:
            self.x = 0

        if pos[1] > self.height * 0.97:
            self.y = -self.speed
        elif pos[1] < self.height * 0.03:
            self.y = self.speed
        else:
            self.y = 0

        self.scroll.x += self.x
        self.scroll.y += self.y
        