# main file / lounch from here
import pygame as pg
from constants import *
from sprites import *


class Game:

	def __init__(self):
		self.runing = True

		# initialization pygame sounds and creat a windows
		pg.init()
		pg.mixer.init()
		self.screen = pg.display.set_mode((WIDTH, HEIGHT))
		self.clock = pg.time.Clock()


	def new(self):
		# start new game
		self.run()

	def run(self):
		# Main loop
		self.playing = True
		while self.playing:
			self.clock.tick(FPS)
			self.events()
			self.update()
			self.draw()



	def update(self):
		# update sprites
		pass

	def events(self):
		# Process input
		for event in pg.event.get():
			if event.type == pg.QUIT:
				if self.playing:
					self.playing = False
				self.runing = False

	def draw(self):
		# draw sprites
		self.screen.fill(WHITE)


		pg.display.flip()

	def show_start_screen(self):
		pass

	def show_gameover_screen(self):
		pass



G = Game()

G.show_start_screen()
while G.runing:
	G.new()
	G.show_gameover_screen()

pg.quit()




