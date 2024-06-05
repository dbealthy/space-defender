# pygame template 
import pygame
import random

WIDTH = 640
HEIGHT = 480
CENTER = ( WIDTH // 2, HEIGHT // 2 )

FPS = 60


#colours
WHITE = ( 255, 255, 255 )
BLUE = ( 0 ,0, 255 )
BLACK = ( 0, 0, 0 )
RED = ( 255, 0, 0 )
YELLOW = ( 255, 255, 0 )
GREEN = ( 0, 255, 0)


# initialization pygame sounds and creat a windows
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()


all_sprites = pygame.sprite.Group()


# Main loop

GameOver = False
while not GameOver:
	# fps
	clock.tick(FPS)
	# Process input
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			GameOver = True
	# Update
	all_sprites.update()
	RANDOM_COLOUR = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

	# Draw / render
	screen.fill((255, 255, 255))
	all_sprites.draw(screen)


	# after all
	pygame.display.flip()



pygame.quit()