import pygame as pg

from constants import *


class Game:

    def __init__(self):
        self.runing = True

        # initialization pygame sounds and creat a windows
        pg.init()
        pg.mixer.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        self.clock = pg.time.Clock()

    def play(self):
        self.show_start_screen()
        while self.runing:
            self.new()
            self.show_gameover_screen()

        pg.quit()

    def new(self):
        # start new game
        self.run()

    def quit(self):
        if self.playing:
            self.playing = False
        self.runing = False

    def run(self):
        self.playing = True
        while self.playing:
            self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()

    def update(self):
        pass

    def events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.quit()

    def draw(self):
        # draw sprites
        self.screen.fill(WHITE)

        pg.display.flip()

    def show_start_screen(self):
        pass

    def show_gameover_screen(self):
        pass
