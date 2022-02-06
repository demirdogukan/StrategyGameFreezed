import pygame as pg
from settings import *
from world import World
from utils import draw_text
from hud import Hud

pg.init()
clock = pg.time.Clock()
screen = pg.display.set_mode((0, 0), pg.FULLSCREEN)
WIDTH, HEIGHT = screen.get_size()

color = pg.Color(0, 0, 0)

class Game:
    def __init__(self, screen, clock) -> None:
        self.screen = screen
        self.clock = clock
        self.condition = "Game"
        self.hud = Hud(screen, WIDTH, HEIGHT, 25, 25)
        self.world = World(screen, 25, 25, WIDTH, HEIGHT, self.hud)
    
    def run(self):
        if self.condition == "Game":
            # draw world
            self.world.draw()
            self.world.update()

            # draw head up display
            self.hud.draw()
            self.hud.update()

game = Game(screen, clock)
while True:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                pg.quit()

    game.run()
    # Draw Fps
    draw_text(screen, f"fps={int(clock.get_fps())}", 25, (255, 255, 255), (25, 25))
    clock.tick(60)
    pg.display.flip()
    pg.display.update()

