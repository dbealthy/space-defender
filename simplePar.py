# pygame template 
import pygame as pg
import random
import qtool
from options import *

class Particle:
	def __init__(self, origin, acc, colour):
		self.origin = origin
		self.colour = colour
		self.position = pg.Vector2(self.origin)
		self.velocity = pg.Vector2()
		self.acceleration = pg.Vector2(acc)


		self.radius = random.randint(1, 4)
		self.surface = pg.Surface((self.radius*2, self.radius*2))
		self.rect = self.surface.get_rect()
		self.surface.set_colorkey(BLACK)
		self.life_time = 255
		self.live_speed = self.life_time / HEIGHT * self.radius


	def update(self):
		self.velocity += self.acceleration * self.radius
		self.position += self.velocity 

		self.life_time -= self.live_speed 

	def draw(self, surf):
		self.surface.set_alpha(self.life_time)
		surf.blit(self.surface, (int(self.position.x), int(self.position.y)))
		pg.draw.circle(self.surface, self.colour, (int(self.rect.center[0]), int(self.rect.center[1])), self.radius)

# initialization pygame sounds and creat a windows
if __name__ == '__main__':
	pg.init()
	pg.mixer.init()
	screen = pg.display.set_mode((WIDTH, HEIGHT))
	clock = pg.time.Clock()

	all_sprites = pg.sprite.Group()
	bg_colour = BLACK

	p = Particle((WIDTH//2, 0))

	# Main loop

	GameOver = False
	while not GameOver:
		# fps
		clock.tick(FPS)
		# Process input
		for event in pg.event.get():
			if event.type == pg.QUIT:
				GameOver = True
		# Update
		all_sprites.update()
		p.update()

		# Draw / render
		screen.fill(bg_colour)
		all_sprites.draw(screen)
		p.draw(screen)


		# after all
		pg.display.flip()



	pg.quit()