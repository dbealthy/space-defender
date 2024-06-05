import pygame


class SpriteSheet():
	def __init__(self, name):
		self.spritesheet = pygame.image.load(name)

	def get_image(self, coords, width, height):
		(x, y) = coords
		image = pygame.Surface((width, height))
		image.blit(self.spritesheet, (0,0), (x, y, width, height))
		return image

def calcPos(width, height, raws, columns):        #if all sprites are the same width and height
	Swidth = width / columns
	Sheight = height / raws
	x = 0
	y = 0
	result = []
	for i in range(raws):
		y = i*Sheight
		for j in range(columns):
			x = j*Swidth
			result.append(tuple((x, y)))
	return result
