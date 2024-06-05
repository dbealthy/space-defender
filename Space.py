# pygame template 
import pygame
import random
import qtool
from simplePar import Particle
from options import *

class ParticleSystem:
	def __init__(self):
		# self.origin = origin
		self.all_particles = []
		self.quntity = 0
		self.colours = (CYAN, GOLD, WHITE, PALERED, DARKGREEN)

	def spawn(self, quntity):
		for i in range(quntity):
			rand_x = random.randrange(0, WIDTH)
			particle_origin = (rand_x, - 25)
			acceleration = (0, random.uniform(0.001, 0.02))
			colour = random.choice(self.colours)
			p = Particle(particle_origin, acceleration, colour)
			self.all_particles.append(p)

	def update(self):
		for p in self.all_particles:
			p.update()

			if p.life_time <= 0:
				self.all_particles.remove(p)

	def draw(self, surf):
		for p in self.all_particles:
			p.draw(surf)




if __name__ == "__main__":
	# initialization pygame sounds and creat a windows
	pygame.init()
	pygame.mixer.init()
	screen = pygame.display.set_mode((WIDTH, HEIGHT))
	clock = pygame.time.Clock()

	all_sprites = pygame.sprite.Group()
	bg_colour = DARKBLUE
	last_upd = pygame.time.get_ticks()
	ps = ParticleSystem((5, - 50))
	# Main loop

	GameOver = False
	while not GameOver:
		# fps
		clock.tick(FPS)
		# Process input
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				GameOver = True

			if event.type == pygame.MOUSEBUTTONDOWN:
				# ps = ParticleSystem(pygame.mouse.get_pos())
				# ps.spawn(15)
				# systems.append(ps)
				pass

		# Update
		now = pygame.time.get_ticks()
		if now - last_upd > 1000:
			last_upd = now
			ps.spawn(15)


		all_sprites.update()
		ps.update()


		# Draw / render
		screen.fill(bg_colour)
		all_sprites.draw(screen)
		ps.draw(screen)


		# after all
		pygame.display.flip()



	pygame.quit()